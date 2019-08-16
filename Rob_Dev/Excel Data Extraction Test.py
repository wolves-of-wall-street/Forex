import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
from pandas import ExcelFile
from datetime import datetime
import math
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

homeCurr = "GBP"
toCurr = "USD"
year = 2017
df_in = pd.read_excel("DAT_XLSX_GBPUSD_M1_2017.xlsx", sheetname = "2017")

timeFrame = 7   #Timeframe (days)

date = df_in.iloc[:,0].tolist()    #The first column in the Excel file contains the dates
exRate = df_in.iloc[:,1].tolist()   #The second column in the Excel file contains the exchage rates
#print(type(date[2]))
#print(exRate[2])

rowIndex = 0     #keeps track of the current row
refDateRow = 1299    #The row that contains the reference data, which is the first date that contains a full 24 hours in the Excel file (the first date in the file starts at 2am, so it does not contain a full day of data; we want timeframes to be on the order of days, so we want timeframes to be cutoff at midnight, that way days are split into two different timeframes)
refDate = pd.to_datetime(date[refDateRow] )   #The reference date is simply the date contained in the refDateRow
#print(type(date[2] - date[1]))

cols = {"Start Date": [], "Open": [], "High": [], "Low": [], "Close": []}    #cols is a dictionary that will contain the OHLC data for the specified timeframe; Start Date will contain the date of the beginning of each time frame


def findHigh(rowIndex):
    checkRowIndex = rowIndex     #The function's "version" of rowIndex; we need to distinguish the two becasue Python passes by value--changing rowIndex in this function will change rowIndex everywhere
    currHighIndex = checkRowIndex     #The index of the High is initially assigned to the first index of the timeframe
    startDate = pd.to_datetime(date[rowIndex])
    checkRowIndex += 1
    currDate = pd.to_datetime(date[checkRowIndex])      #The date of the row we are currently checking
    while((currDate - startDate).total_seconds() < timeFrame*24*60*60):     #Ensures that we only the dates within this timeframe
        if exRate[checkRowIndex] > exRate[currHighIndex]:
            currHighIndex = checkRowIndex               #Update the current high
            checkRowIndex += 1                          #Update the row we are checking...
            currDate = pd.to_datetime(date[checkRowIndex])    #...and update the date
        else:
            checkRowIndex += 1                          #Update the row we are checking...
            currDate = pd.to_datetime(date[checkRowIndex])    #...and update the date
    return exRate[currHighIndex]     #We need to return the actual high exchange rate, not its index
    


def findLow(rowIndex):
    checkRowIndex = rowIndex     #The function's "version" of rowIndex; we need to distinguish the two becasue Python passes by value--changing rowIndex in this function will change rowIndex everywhere
    currLowIndex = checkRowIndex     #The index of the low is initially assigned to the first index of the timeframe
    startDate = pd.to_datetime(date[rowIndex])
    checkRowIndex += 1
    currDate = pd.to_datetime(date[checkRowIndex])      #The date of the row we are currently checking
    while((currDate - startDate).total_seconds() < timeFrame*24*60*60):     #Ensures that we only the dates within this timeframe
        if exRate[checkRowIndex] < exRate[currLowIndex]:
            currLowIndex = checkRowIndex               #Update the current low
            checkRowIndex += 1                          #Update the row we are checking...
            currDate = pd.to_datetime(date[checkRowIndex])    #...and update the date
        else:
            checkRowIndex += 1                          #Update the row we are checking...
            currDate = pd.to_datetime(date[checkRowIndex])    #...and update the date
    return exRate[currLowIndex]     #We need to return the actual low exchange rate, not its index
    
    

def findClose(rowIndex):
    checkRowIndex = rowIndex     #The function's "version" of rowIndex; we need to distinguish the two becasue Python passes by value--changing rowIndex in this function will change rowIndex everywhere
    startDate = pd.to_datetime(date[rowIndex])
    checkRowIndex += 1
    currDate = pd.to_datetime(date[checkRowIndex])      #The date of the row we are currently checking
    while((currDate - startDate).total_seconds() < timeFrame*24*60*60):     #Ensures that we only the dates within this timeframe
            checkRowIndex += 1                          #Update the row we are checking...
            currDate = pd.to_datetime(date[checkRowIndex])    #...and update the date
    return exRate[checkRowIndex - 1]     #We need to return the actual close rate, not its index
                                         #We do minus 1 because when the while loop finishes, checkRowIndex will be at the index of the beginning of the next timeframe; the closing index the is the index before that, hence we do minus 1


#Loop to collect all of the OHLC data into cols:
while(rowIndex < len(date)):
    thisRowDate = pd.to_datetime(date[rowIndex])
    if (thisRowDate - refDate).total_seconds() >= 0.0:
        if (thisRowDate - refDate).total_seconds()%(timeFrame*24*60*60) == 0.0:      #If the date of the current row is at or beyond the reference date and exactly timeFrame number of days from it...
            cols["Start Date"].append(thisRowDate)                      #...then this date is the beginning of a new time frame. Find the Open, Close, High, and Low for this time frame
            cols["Open"].append(exRate[rowIndex])
            cols["High"].append(findHigh(rowIndex))
            cols["Low"].append(findLow(rowIndex))
            cols["Close"].append(findClose(rowIndex))
            rowIndex += 1
        else:
            rowIndex += 1
    else:
        rowIndex += 1
 
    

data_df = pd.DataFrame(cols)
print(data_df.head(30))

#SETUP THE CANDLESTICK GRAPH:
data_df['Start Date'] = pd.to_datetime(data_df['Start Date'])
data_df["Start Date"] = data_df["Start Date"].apply(mdates.date2num)
# Creating required data in new DataFrame OHLC
ohlc= data_df[['Start Date', 'Open', 'High', 'Low','Close']].copy()
f1, ax = plt.subplots(figsize = (10,5))

# plot the candlesticks
candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.title("Exchange Rate of " + homeCurr + " Relative to " + toCurr + ", Daily OHLC (" + str(year) + "). Timeframe: " + str(timeFrame) + " days")
plt.xlabel("Date")
plt.ylabel("Exchange Rate")
plt.show()