# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eQTzxw6QK4d9Gp6vtIMOUx0ZyE40dUq6
"""

pip install yfinance

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

stock = yf.Ticker("AAPL")
data = stock.history(period="1y")
print(data.head())

"""# Calculation of momentum"""

data['momentum'] = data['Close'].pct_change()

# Creating subplots to show momentum and buying/selling markers
figure = make_subplots(rows=2, cols=1)
figure.add_trace(go.Scatter(x=data.index,
                         y=data['Close'],
                         name='Close Price'))
figure.add_trace(go.Scatter(x=data.index,
                         y=data['momentum'],
                         name='Momentum',
                         yaxis='y2'))
# Adding the buy and sell signals
figure.add_trace(go.Scatter(x=data.loc[data['momentum'] > 0].index,
                         y=data.loc[data['momentum'] > 0]['Close'],
                         mode='markers', name='Buy',
                         marker=dict(color='green', symbol='triangle-up')))

figure.add_trace(go.Scatter(x=data.loc[data['momentum'] < 0].index,
                         y=data.loc[data['momentum'] < 0]['Close'],
                         mode='markers', name='Sell',
                         marker=dict(color='red', symbol='triangle-down')))

figure.update_layout(title='Algorithmic Trading using Momentum Strategy',
                     xaxis_title='Date',
                     yaxis_title='Price',

                     )
figure.update_yaxes(title="Momentum", secondary_y=True)
figure.show()

"""# Calculate CAGR"""

initial_value = df['Close'].iloc[0]  # First row's close price
final_value = df['Close'].iloc[-1]    # Last row's close price

# Since we are considering one year
years = 1
# Calculate CAGR
cagr = (final_value / initial_value) ** (1 / years) - 1

# Convert to percentage
cagr_percentage = cagr * 100
print(f"CAGR: {cagr_percentage:.2f}%")

"""This indicates that the investment grew at an average annual rate of 37% over the specified period of one year.

#Calculation of Moving Average
"""

data['Moving_Average'] = data['Close'].rolling(window=10).mean()

# Create figure
figure = go.Figure()

# Plot Close Price
figure.add_trace(go.Scatter(x=data.index,
                             y=data['Close'],
                             name='Close Price',
                             line=dict(color='yellow')))

# Plot Moving Average
figure.add_trace(go.Scatter(x=data.index,
                             y=data['Moving_Average'],
                             name='Moving Average',
                             line=dict(color='black', dash='dash')))

# Update layout
figure.update_layout(title='Close Price and Moving Average',
                     xaxis_title='Date',
                     yaxis_title='Price')

# Show the figure
figure.show()

# Define signals for trading
data['Signal'] = 0  # Initialize the Signal column

# Generate buy/sell signals based on moving average
data.loc[data['Close'] > data['Moving_Average'], 'Signal'] = 1  # Buy
data.loc[data['Close'] < data['Moving_Average'], 'Signal'] = -1  # Sell

# Calculate returns
data['Position'] = data['Signal'].shift()  # Shift signals for alignment
data['Daily_Return'] = data['Close'].pct_change()
data['Strategy_Return'] = data['Position'] * data['Daily_Return']

# Calculate cumulative returns
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod()

data['Cumulative_Strategy_Return'] = data['Cumulative_Strategy_Return'].fillna(data['Cumulative_Strategy_Return'].mean())
data['Cumulative_Strategy_Return'].isnull().sum()

"""# Calculate CAGR"""

start_value = data['Cumulative_Strategy_Return'].iloc[0]
end_value = data['Cumulative_Strategy_Return'].iloc[-1]
n_years = len(data) / 252  # Assuming daily data (252 trading days in a year)

# CAGR calculation
cagr = (end_value / start_value) ** (1 / n_years) - 1
cagr_percentage = cagr * 100

print(f"CAGR for Moving Average Strategy: {cagr_percentage:.2f}%")
