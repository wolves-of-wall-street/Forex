import bs4
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
from lxml import html
import requests

#Webscraper for xe.com



#These strings will be used to help build the URL
from_currency = "USD"     #This program will calculate the exchange rate of ONE currency, which you specify, with respect to a list of OTHER currencies, which you can add to
to_currency_list = ["CAD", "EUR", "GBP"]

#These strings will be used to help build the URL
view_list = ["12h", "1D", "1W", "1M", "1Y", "2Y", "5Y", "10Y"]   #List of the various time frames that XE provides


for toCurr in to_currency_list:
    for view in view_list:
        my_url = "https://www.xe.com/currencycharts/?from=" + from_currency + "&to=" + toCurr + "&view=" + view
        #page = requests.get(my_url)        #Open webpage
        #tree = html.fromstring(page.content)
        #low = tree.xpath('//*[@id="rates_detail_desc"]/strong[3]')
        #high = tree.xpath('//*[@id="rates_detail_desc"]/strong[4]')
        #print(low)
        
        
        
        
        uClient = uReq(my_url)        #Open webpage
        page_html = uClient.read()    #Read webpage
        uClient.close()               #Close webpage
        page_soup = soup(page_html, "html.parser")    #html parsing
        rates_detail = page_soup.find("div", {"id": "rates_detail_desc"})
        inner_text = rates_detail.text
        #rates_detail = page_soup.find("table", {"id": "crLive"})
        #rate = rates_detail.tbody
        print(inner_text)