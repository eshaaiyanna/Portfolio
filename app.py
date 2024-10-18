from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import uuid
import openai
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# # env_vars = dict(os.environ)
# # print(env_vars)

# # OR iterate and print
# for key, value in os.environ.items():
#     print(f"{key}={value}")

openai.api_key = os.environ.get("openai_key")

print(os.environ.get("user"))
print(os.environ["password"])

# Connect to PostgreSQL database
conn = psycopg2.connect(
    database="chatbot_db",
    user=os.environ.get("user"),
    password=os.environ.get("password"),
    host="localhost",
    port="5432"
)

app = Flask(__name__, template_folder='.')
CORS(app)

conversations = []




@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('indexcheck.html')

@app.route('/chat', methods=['POST'])
def chat():
    
    user_input = request.json['user_input']
    user_id = request.json['user_id']
    session_id = request.json['session_id']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate conversation ID
    conversation_id = str(uuid.uuid4())

    # Modified chatbot logic
    if "hi" in user_input.lower():
        bot_response = "Hello! How can I assist you?"
    elif "how are you" in user_input.lower():
        bot_response = "I'm just a computer program, so I don't have feelings. But thanks for asking!"
    else:
        # bot_response = "I'm sorry, I don't understand that command."
        
        # OpenAI GPT-3 logic starts here
        # model_engine = "text-davinci-002"  # Use the engine you prefer
        model_engine="davinci-codex"
        prompt = user_input
        max_tokens = 1000  # You can set the max tokens as per your needs

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_tokens
        )
        
        bot_response = response.choices[0].text.strip()

    # Save conversation
    conversations.append({
        'user_input': user_input,
        'bot_response': bot_response,
        'user_id': user_id,
        'session_id': session_id,
        'conversation_id': conversation_id,
        'timestamp': timestamp,
    })
    
    # Insert conversation into PostgreSQL
    cursor = conn.cursor()
    insert_query = """INSERT INTO conversations (user_input, bot_response, user_id, session_id, conversation_id, timestamp) VALUES (%s, %s, %s, %s, %s, %s);"""
    cursor.execute(insert_query, (user_input, bot_response, user_id, session_id, conversation_id, timestamp))
    conn.commit()

    return jsonify({'bot_response': bot_response, 'user_id': user_id, 'conversation_id': conversation_id, 'timestamp': timestamp})

@app.route('/fetch_previous_chats', methods=['POST'])
def fetch_previous_chats():
    data = request.json
    # user_id = data.get('user_id')
    session_id = data.get('session_id')
    
    print(f'Session id : {session_id}')
    
    cursor = conn.cursor()
    
    query = f"""SELECT  user_id, user_input, bot_response FROM conversations WHERE session_id = '{session_id}'"""
    cursor.execute(query)
    
    chat_data = cursor.fetchall()
    cursor.close()
    
    print(chat_data)
    
    previous_chats_html = ""
    user_id = None  # Initialize to None, will be set based on the SQL result
    
    for fetched_user_id, user_msg, bot_msg in chat_data:
        if user_id is None:
            user_id = fetched_user_id  # Set the user_id based on the first record
        
        previous_chats_html += f"You: {user_msg}<br>Bot: {bot_msg}<br>"
    
    return jsonify({
        'previous_chats': previous_chats_html, 
        'session_id': session_id,
        'user_id': user_id  # Sending back user_id to the frontend
    })
    
@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    data = request.json
    session_id = data.get('session_id')
    conversation_id = data.get('conversation_id')
    feedback = data.get('feedback')  # This will be either 'thumbs_up' or 'thumbs_down'
    
    # Store the feedback in your database, log, or any other storage linked with the session_id and conversation_id
    # ... your code to store feedback ...

    return jsonify({"status": "success", "message": "Feedback received"})



if __name__ == '__main__':
    app.run(debug=True)
