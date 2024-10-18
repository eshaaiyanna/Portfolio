from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import uuid
import openai
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Connect to PostgreSQL database
conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

app = Flask(__name__, template_folder='.')
CORS(app)

# Route to serve the index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Extract data from request
        user_input = request.json['user_input']
        user_id = request.json['user_id']
        session_id = request.json['session_id']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conversation_id = str(uuid.uuid4())

        # Perform chatbot logic (example shown with OpenAI)
        if "hi" in user_input.lower():
            bot_response = "Hello! How can I assist you?"
        elif "how are you" in user_input.lower():
            bot_response = "I'm just a computer program, so I don't have feelings. But thanks for asking!"
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
            )
            bot_response = response['choices'][0]['message']['content'].strip()

        # Insert conversation into PostgreSQL
        cursor = conn.cursor()
        insert_query = """INSERT INTO chatbot_conversations (user_input, bot_response, user_id, session_id, conversation_id, timestamp) 
                          VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(insert_query, (user_input, bot_response, user_id, session_id, conversation_id, timestamp))
        conn.commit()

        cursor.close()

        # Return bot response
        return jsonify({'bot_response': bot_response, 'user_id': user_id, 'conversation_id': conversation_id, 'timestamp': timestamp})

    except Exception as e:
        # Handle and log any exceptions
        print(f"Error in /chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

# Route to fetch previous chats
@app.route('/fetch_previous_chats', methods=['POST'])
def fetch_previous_chats():
    try:
        data = request.json
        session_id = data.get('session_id')

        cursor = conn.cursor()
        query = """SELECT user_input, bot_response FROM chatbot_conversations WHERE session_id = %s"""
        cursor.execute(query, (session_id,))
        chat_data = cursor.fetchall()
        cursor.close()

        previous_chats = []
        for user_input, bot_response in chat_data:
            previous_chats.append({'user_input': user_input, 'bot_response': bot_response})

        return jsonify({'previous_chats': previous_chats})

    except Exception as e:
        # Handle and log any exceptions
        print(f"Error in /fetch_previous_chats endpoint: {e}")
        return jsonify({'error': str(e)}), 500

# Route to send feedback
@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    try:
        data = request.json
        session_id = data.get('session_id')
        conversation_id = data.get('conversation_id')
        feedback = data.get('feedback')  # This will be either 'thumbs_up' or 'thumbs_down'

        # Your logic to store feedback in the database

        return jsonify({"status": "success", "message": "Feedback received"})

    except Exception as e:
        # Handle and log any exceptions
        print(f"Error in /send_feedback endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
