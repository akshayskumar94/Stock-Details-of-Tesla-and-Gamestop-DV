#!/usr/bin/env python
# coding: utf-8

# # Extracting and Visualising Stock and Revenue Data
# ***Using Tesla and Gamestop as example***

# Entering 2021 we have seen a huge surge in the share prices of Tesla and Gamestop, Let us compare this surge with the quarterly revenue data for the respective companies using Data Scraping and Data Visualisation Techniques.

# ***Install necessary packages***

# In[1]:


get_ipython().system('pip install yfinance')
#!pip install pandas
#!pip install requests
get_ipython().system('pip install bs4')
#!pip install plotly


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ***Defining the graph function***

# In[3]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ***Extracting Tesla Stock Data***

# In[5]:


data=yf.Ticker("TSLA")


# In[6]:


tesla_data=data.history(period='max')
tesla_data.reset_index(inplace=True)
tesla_data.head()


# ***Webscraping using beautifulsoup to extract tesla quarterly revenue***

# In[11]:


data1=requests.get('https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue').text
soup=BeautifulSoup(data1,'html5lib') #Parsing withbeautiful soup
tables = soup.find_all('table')
data=pd.read_html(str(tables[1]), flavor='bs4') #Selecting tables with revenue data
tesla_revenue=data[0] #Extracting tesla quarterly revenue
tesla_revenue.columns=["Date","Revenue"]
tesla_revenue["Revenue"]=tesla_revenue["Revenue"].str.replace('$',"").str.replace(",","") #Removing special charatcer from Revenue
tesla_revenue.dropna(subset=['Revenue'], inplace=True) #Removing Null values
print(tesla_revenue)


# ***Extracting Gamestop Stock Data***

# In[12]:


data=yf.Ticker("GME")
gme_data=data.history(period='max')
gme_data.reset_index(inplace=True)
gme_data.head()


# ***Webscraping using beautifulsoup to extract GameStop quarterly revenue***

# In[14]:


url="https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data=requests.get(url).text
soup=BeautifulSoup(html_data,"html5lib") #Parsing with beautiful soup
tables=soup.find_all("table")
data=pd.read_html(str(tables[1]), flavor='bs4') #Selecting tables with revenue data
gme_revenue=data[0] #Extracting quarterly revenue
gme_revenue.columns=["Date","Revenue"]
gme_revenue["Revenue"]=gme_revenue["Revenue"].str.replace('$','').str.replace(",","") #Removing special characters
gme_revenue.dropna(subset=['Revenue'], inplace=True) #Removing NULL values
print(gme_revenue)


# ***Plotting graphs of Historical Share Price and Historical Revenue for Tesla and GameStop***

# In[15]:


make_graph(tesla_data,tesla_revenue,'Tesla')


# In[16]:


make_graph(gme_data,gme_revenue,'GameStop')

