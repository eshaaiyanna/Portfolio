# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1smM5Pl7nmYRWHeHR6ZQgycwvB8F65DXb
"""

import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_white"

cd = pd.read_csv("/content/control_group.csv",sep = ";")
td = pd.read_csv("/content/test_group.csv",sep = ";")

cd.shape

td.head()

cd.columns = ["Campaign Name", "Date", "Amount Spent",
                        "Number of Impressions", "Reach", "Website Clicks",
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]

td.columns = ["Campaign Name", "Date", "Amount Spent",
                        "Number of Impressions", "Reach", "Website Clicks",
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]

"""Data Cleaning"""

cd.isnull().sum()

cd.dtypes

col = cd[["Number of Impressions","Reach","Website Clicks","Searches Received","Content Viewed","Added to Cart","Purchases"]]
# print(col.head())
# print(col.shape)
# print(col.index)

for i in col:
  col[i] = col[i].fillna(col[i].mean())

cd1 =  cd[["Campaign Name","Date","Amount Spent"]]
print(cd.head())
print(cd.shape)
print(cd.index)

cd1.reset_index(drop = True,inplace = True)
col.reset_index(drop = True,inplace = True)

cd2 = pd.concat([cd1,col],axis = 1)

cd2.head()

td.isnull().sum()

abd = cd2.merge(td,how = 'outer').sort_values(['Date'])
abd.reset_index(drop = True,inplace = True)
abd.head()

abd['Campaign Name'].value_counts()

figure = px.scatter(data_frame=abd,
                    x="Number of Impressions",
                    y="Amount Spent",
                    size="Amount Spent",
                    color="Campaign Name",
                    trendline="ols",
                    title="Scatter Plot of Impressions vs Amount Spent")
figure.show()

"""The control campaign resulted in more impressions wrt to the amount spent on both campaigns."""

label = ["Total Searches from Control Campaign",
         "Total Searches from Test Campaign"]
counts = [cd2['Searches Received'].sum(),td['Searches Received'].sum()]
colors = ['pink','lightblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Searches Recieved')
fig.update_traces(hoverinfo='label + value', textinfo='percent',
                  textfont_size=30,
                  marker=dict(colors=colors,
                              line=dict(color='black', width=1)))
fig.show()

label = ["Website Clicks from Control Campaign",
         "Website Clicks from Test Campaign"]
counts = [cd2['Website Clicks'].sum(),td['Website Clicks'].sum()]
colors = ['pink','lightblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Website Clicks')
fig.update_traces(hoverinfo='label + value', textinfo='percent',
                  textfont_size=30,
                  marker=dict(colors=colors,
                              line=dict(color='black', width=1)))
fig.show()

label = ["Content Viewed from Control Campaign",
         "Content Viewed from Test Campaign"]
counts = [sum(cd2["Content Viewed"]),
          sum(td["Content Viewed"])]
colors = ['pink','lightblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Content Viewed')
fig.update_traces(hoverinfo='label + value', textinfo='percent',
                  textfont_size=30,
                  marker=dict(colors=colors,
                              line=dict(color='black', width=1)))
fig.show()

label = ["Products Added to Cart from Control Campaign",
         "Products Added to Cart from Test Campaign"]
counts = [sum(cd2["Added to Cart"]),
          sum(td["Added to Cart"])]
colors = ['pink','lightblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Added to Cart')
fig.update_traces(hoverinfo='label + value', textinfo='percent',
                  textfont_size=30,
                  marker=dict(colors=colors,
                              line=dict(color='black', width=1)))
fig.show()

label = ["Amount Spent in Control Campaign",
         "Amount Spent in Test Campaign"]
counts = [sum(cd2["Amount Spent"]),
          sum(td["Amount Spent"])]
colors = ['pink','lightblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Amount Spent')
fig.update_traces(hoverinfo='label+value', textinfo='percent',
                  textfont_size=30,
                  marker=dict(colors=colors,
                              line=dict(color='black', width=1)))
fig.show()

label = ["Purchases Made by Control Campaign",
         "Purchases Made by Test Campaign"]
counts = [sum(cd2["Purchases"]),
          sum(td["Purchases"])]
colors = ['pink','lightblue']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Purchases')
fig.update_traces(hoverinfo='label+value', textinfo='percent',
                  textfont_size=30,
                  marker=dict(colors=colors,
                              line=dict(color='black', width=1)))
fig.show()

"""Relationship between the number of website clicks and content viewed from both campaigns:"""

figure = px.scatter(data_frame = abd,
                    x="Content Viewed",
                    y="Website Clicks",
                    size="Website Clicks",
                    color= "Campaign Name",
                    trendline="ols",title="Content Viewed vs Website Clicks")

figure.show()

"""Conetnt viewed is higher in the control campaign"""

figure = px.scatter(data_frame = abd,
                    x="Added to Cart",
                    y="Content Viewed",
                    size="Added to Cart",
                    color= "Campaign Name",
                    trendline="ols",
                    title="Content Viewed vs Added to Cart")
figure.show()

"""Control Campaign has more items added to the cart"""

figure = px.scatter(data_frame = abd,
                    x="Purchases",
                    y="Added to Cart",
                    size="Purchases",
                    color= "Campaign Name",
                    trendline="ols",
                    title = "Added to Cart vs Purchases")
figure.show()

"""Although the control campaign resulted in more sales and more products in the cart, the conversation rate of the test campaign is higher

From the above A/B tests, we found that the control campaign resulted in more sales and engagement from the visitors. More products were viewed from the control campaign, resulting in more products in the cart and more sales. But the conversation rate of products in the cart is higher in the test campaign. The test campaign resulted in more sales according to the products viewed and added to the cart. And the control campaign results in more sales overall. So, the Test campaign can be used to market a specific product to a specific audience, and the Control campaign can be used to market multiple products to a wider audience.
"""