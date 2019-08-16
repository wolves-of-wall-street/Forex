import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import bs4
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
from lxml import html
import requests


#Webscraping from myfxbook.com
homeCurr = "EUR"      #Currency that the exchange rate pertains to
toCurr = "USD"       #Currency that the exchange rate is relative to

myURL = "https://www.myfxbook.com/en/forex-market/currencies/" + homeCurr +toCurr + "-historical-data"
print(myURL)
page = requests.get(myURL)        #Open webpage
content = html.fromstring(page.content)      #Store the contents of the webpage
#tr_elements = content.xpath('//tr')           #Parse data that are stored between <tr>..</tr> of HTML
#firstRow = 3    #First row of the table we are looking for (header row)





#The first row contains the headers:
#col = []      #List that will contain column headers
#i = 0

#Store the headers in col:
#for t in tr_elements[firstRow]:     #The headers are in the first row, but the main table is NOT the only table on the website; it's actually the fourth, hence the 3 index (instead of 0)
#    header = t.text_content()
#    print(header)
#    col.append(col, [])
    
    
#just manually define the columns, since you already know what they are:
cols = {"Date": [], "Open": [], "High": [], "Close": []}      #The [] are empty lists that will eventually contain the data in that column

#for i in range(firstRow+1,len(tr_elements)):   #This first row of actual data is at index firstRow + 1 because firstRow is just the header row
#    row = tr_elements[i]
    
#    colIndex = 0   #Index of the column we are traversing through
    
#    for t in row.iterchildern():
#        data = t.text_content()
     
#        if i > 0:              #All data past the first column must be converted to floats(decimals); the first column is a timestamp, which is its own datatype
#            data = float(data)
        
#        col[colIndex][i] = data     #Append the data to the list of the colIndex column
#        colIndex += 1               #Increment colIndex
        




#web_df = pd.DataFrame(cols)
#web_df.head()      
