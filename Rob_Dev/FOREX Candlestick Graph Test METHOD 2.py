import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import bs4
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
from lxml import html
import requests
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates


#Webscraping from myfxbook.com
homeCurr = "EUR"      #Currency that the exchange rate pertains to
toCurr = "USD"       #Currency that the exchange rate is relative to

myURL = "https://www.myfxbook.com/en/forex-market/currencies/" + homeCurr +toCurr + "-historical-data"
print(myURL)
uClient = uReq(myURL)        #Open webpage
page_html = uClient.read()    #Read webpage
uClient.close()               #Close webpage
page_soup = soup(page_html, "html.parser")    #html parsing
dataTable = page_soup.find("table", {"id": "symbolMarket"})    #METHOD 2

#just manually define the columns, since you already know what they are:
cols = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}      #The [] are empty lists that will eventually contain the data in that column


#METHOD 2:
for row in dataTable.find_all("tr"):
    if len(row.find_all("td")) > 0:     
        #print(row.find("span", {"name": "time" + homeCurr + toCurr}).get_text())
        cols["Date"].append(row.find("span", {"name": "time" + homeCurr + toCurr}).get_text())     #NOTE:THIS CODE AUTOMATICALLY SELECTS THE "1 DAY" TIMEFRAME, SO DATAPOINTS ARE EACH SEPARATED BY 24 HOURS; NOT SURE HOW TO CHANGE THE TIMEFRAME IN THE CODE
        cols["Open"].append(float(row.find("span", {"name": "open" + homeCurr + toCurr}).get_text()))
        cols["High"].append(float(row.find("span", {"name": "high" + homeCurr + toCurr}).get_text()))
        cols["Low"].append(float(row.find("span", {"name": "low" + homeCurr + toCurr}).get_text()))
        cols["Close"].append(float(row.find("span", {"name": "close" + homeCurr + toCurr}).get_text()))
        print((float(row.find("span", {"name": "high" + homeCurr + toCurr}).get_text())-float(row.find("span", {"name": "low" + homeCurr + toCurr}).get_text()))/float(row.find("span", {"name": "high" + homeCurr + toCurr}).get_text()))
        
        
        
web_df = pd.DataFrame(cols)
web_df.head()



#SETUP THE CANDLESTICK GRAPH:
web_df['Date'] = pd.to_datetime(web_df['Date'])
web_df["Date"] = web_df["Date"].apply(mdates.date2num)
# Creating required data in new DataFrame OHLC
ohlc= web_df[['Date', 'Open', 'High', 'Low','Close']].copy()
f1, ax = plt.subplots(figsize = (10,5))

# plot the candlesticks
candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.title("Exchange Rate of " + homeCurr + " Relative to " + toCurr + ", Daily OHLC")
plt.show()