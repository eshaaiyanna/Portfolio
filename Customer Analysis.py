#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import mysql.connector
import os

# List of CSV files and their corresponding table names
csv_files = [
    ('customers.csv', 'customers'),
    ('geolocation.csv','geolocation'),
    ('orders.csv', 'orders'),
    ('order_items.csv', 'orders_items'),
    ('sellers.csv', 'sellers'),
    ('products.csv', 'products'),
    ('payments.csv', 'payments')  
   ]

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='ecommerce_db'
)
cursor = conn.cursor()


# Folder containing the CSV files
folder_path ='C:/Users/Admin/Desktop/Ecommerce'

def get_sql_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'INT'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DATETIME'
    else:
        return 'TEXT'

for csv_file, table_name in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Replace NaN with None to handle SQL NULL
    df = df.where(pd.notnull(df), None)
    
    # Debugging: Check for NaN values
    print(f"Processing {csv_file}")
    print(f"NaN values before replacement:\n{df.isnull().sum()}\n")

    # Clean column names
    df.columns = [col.replace(' ', '_').replace('-', '_').replace('.', '_') for col in df.columns]

    # Generate the CREATE TABLE statement with appropriate data types
    columns = ', '.join([f'`{col}` {get_sql_type(df[col].dtype)}' for col in df.columns])
    create_table_query = f'CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})'
    cursor.execute(create_table_query)

    # Insert DataFrame data into the MySQL table
    for _, row in df.iterrows():
        # Convert row to tuple and handle NaN/None explicitly
        values = tuple(None if pd.isna(x) else x for x in row)
        sql = f"INSERT INTO `{table_name}` ({', '.join(['`' + col + '`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(row))})"
        cursor.execute(sql, values)

    # Commit the transaction for the current CSV file
    conn.commit()

# Close the connection
conn.close()


# In[2]:


pip install mysql-connector-python


# In[12]:


import pandas as pd
import seaborn as sns
import mysql.connector
import matplotlib.pyplot as plt


# In[13]:


db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='ecommerce_db'
)


# In[17]:


cur = db.cursor()


# # List all unique cities where customers are located.

# In[64]:


query = """ select distinct(customer_city) from customers"""
cur.execute(query)
data = cur.fetchall()
data = pd.DataFrame(data)
data.head()


# In[20]:


#Count no of orders placed in 2017


# In[30]:


query = """ select count(order_id) from orders
where year(order_purchase_timestamp) = 2017"""
cur.execute(query)
data = cur.fetchall()
data

data[0][0]


# In[31]:


#Find the total sales per category


# In[100]:


query = """select upper(pr.product_category) ,
round(sum(p.payment_value),2) as sales from orders_items as o
join products pr
on o.product_id = pr.product_id
join payments p 
on p.order_id = o.order_id
group by 1"""
cur.execute(query)
data = cur.fetchall()
data
df = pd.DataFrame(data,columns=['Category','Total sales'])
df


# In[38]:


#Calculate the percentage of orders that were paid in installments


# In[46]:


query = """ select sum(case when payment_installments >=1 then 1 else 0 end)/count(*)*100 as payment1
from payments"""
cur.execute(query)
data = cur.fetchall()
data
data[0][0]


# In[47]:


#Count no of customer in each state


# In[59]:


query = """ select customer_state,count(distinct(customer_id)) from customers
group by customer_state"""
cur.execute(query)
data = cur.fetchall()
data = pd.DataFrame(data,columns= ['State','Customers'])
data = data.sort_values(by = 'Customers',ascending = False)


# In[60]:


plt.figure(figsize=(10,8))
sns.barplot(x='State',y = 'Customers',data = data)

Calculate the number of orders per month in 2018
# In[82]:


query = """select year(order_purchase_timestamp) as yr ,count(order_id) as cnt,
monthname(order_purchase_timestamp) as months from orders
where year(order_purchase_timestamp) = 2018
group by 1,3
order by months asc"""
cur.execute(query)
data = cur.fetchall()
data

df = pd.DataFrame(data,columns = ['year','count','months'])
df


# In[97]:


ax = sns.barplot(x = 'months',y='count',data = df)
plt.xticks(rotation = 90)
ax.bar_label(ax.containers[0])
plt.title('Number of orders per month in 2018')
plt.show


# In[98]:


#Find the avg nmber of products,per order grouped by customer city


# In[103]:


query = """select upper(pr.product_category),
round(sum(p.payment_value)/(select sum(payment_value) from payments),2)*100 as persales from orders_items as o
join products pr
on o.product_id = pr.product_id
join payments p 
on p.order_id = o.order_id
group by 1"""
cur.execute(query)
data = cur.fetchall()
data

data = pd.DataFrame(data,columns=['Category','Tot_revenue'])
data


# In[105]:


sns.barplot(x='Category',y ='Tot_revenue',data=data)


# In[111]:


import numpy as np

query = """select products.product_category,count(orders_items.product_id),
round(avg(orders_items.price),2) from products
join orders_items on products.product_id = orders_items.product_id
group by 1 """
cur.execute(query)
data = cur.fetchall()
df = pd.DataFrame(data,columns = ['Category','Count','Price'])
df

arr1 = df['Count']
arr2 = df['Price']

np.corrcoef(df['Count'],df['Price'])


# In[118]:


query = """with cte as (select orders_items.seller_id,sum(payments.payment_value) as tot from orders_items
join payments on payments.order_id = orders_items.order_id
group by 1)

select * ,rank() over( order by tot desc ) as rnk 
from cte """
cur.execute(query)
data = cur.fetchall()
df = pd.DataFrame(data,columns = ['Seller_id','Revenue','Rank'])
df

sns.barplot(x = 'Seller_id',y = 'Revenue',data = df.head(5))
plt.xticks(rotation = 90)
plt.show()

Moving avg of order vales for each customer.
# In[123]:


query = """with cte as 
(select orders.customer_id,payments.payment_value ,orders.order_purchase_timestamp
from orders join payments on orders.order_id = payments.order_id)
select customer_id,order_purchase_timestamp,payment_value,
avg(payment_value) over(partition by customer_id order by order_purchase_timestamp 
rows between 2 preceding and current row) as movavg from cte """
cur.execute(query)
data = cur.fetchall()
data
df = pd.DataFrame(data)
df.head(5)


# In[ ]:




