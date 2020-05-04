import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from nsepy import get_history
from datetime import datetime as dt 

plt.style.use("seaborn")

start_date = dt(2000,1,1)
end_date = dt.now()


# df = get_history("Nifty",start_date,end_date,index=True)

# print(df.tail())

# df.to_csv("Nifty50.csv")

def eichermot():


    df = pd.read_csv("./data/EICHERMOT.csv",parse_dates=True,index_col=0)



    df = df.resample('W').mean()
    # print(df.head())


    fig = plt.figure(figsize=(12,6))
    plt.plot(df.index,df['Close'])
    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.title("Eichermotors stock price over the years")
    # plt.show()

    #Calculate a 50 day moving average
    df['50ma'] = df['Close'].rolling(window=50).mean()

    print(df.tail())

    fig = plt.figure(figsize=(12,6))
    ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)

    ax1.plot(df.index,df['Close'])
    ax1.plot(df.index,df['50ma'])
    ax2.plot(df.index,df['Volume'])

    plt.show()


df = pd.read_csv("./Nifty50_combined.csv",parse_dates=True,index_col=0)

df = df["2010-01-01":"2019-12-31"]

print(df.head())



print("Summary Statistics of 50 stocks:")
print(df.describe().T)

#Plot average price of stocks

summary = df.describe().T

fig = plt.figure(figsize=(8,12))
plt.barh(summary.index,summary['mean'])
plt.title("Average price of Stocks")
plt.ylabel("Stocks")
plt.xlabel("Average price")
# plt.show()

#calculate simple returns or percentage returns of the stocks
fig2 = plt.figure()
df.pct_change().mean().plot(figsize=(10,6),kind='bar')
plt.xlabel("Stocks")
plt.ylabel("Percentage Change")
# plt.show()



#calculate and plot the log returns 
rets = np.log(df/df.shift(1))
rets[rets.columns[30:45]].cumsum().apply(np.exp).plot(figsize=(10,6))
# plt.show()



# select some well performing stocks overtime

print(df.columns)

stocks = df[['SHREECEM','BAJAJFINSV','EICHERMOT','INDUSINDBK','HINDUNILVR']]


ax = stocks.plot(figsize=(10,8),subplots=True,title="Well performing stocks over the past years")
ax[2].set_ylabel("Stock Price")

# plt.show()


#Simple moving average stratergy
#Rolling statistics 


EM = df[:]['SHREECEM'].reset_index()

EM.set_index('Date',inplace=True)

# print(EM.head())


window = 30

EM['min'] = EM['SHREECEM'].rolling(window=window).min()
EM['max'] = EM['SHREECEM'].rolling(window=window).max()
EM['mean'] = EM['SHREECEM'].rolling(window=window).mean()
EM['std'] = EM['SHREECEM'].rolling(window=window).std()
EM['median'] = EM['SHREECEM'].rolling(window=window).median()
EM['ewma'] = EM['SHREECEM'].ewm(halflife=0.5,min_periods=window).mean()


ax = EM[['min','mean','max']].iloc[-750:-350].plot(figsize=(10,6), style=['g--','r--','g--'], lw=0.8)
EM['SHREECEM'].iloc[-750:-350].plot(ax=ax, lw=2)
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("30 days max min simple moving average")
# plt.show()

# moving average cross over

EM['SMA1'] = EM['SHREECEM'].rolling(window=52).mean()
EM['SMA2'] = EM['SHREECEM'].rolling(window=252).mean()

EM.dropna(inplace=True)

EM['positions'] = np.where(EM['SMA1']>EM['SMA2'],1,-1)




ax = EM[['SHREECEM','SMA1','SMA2','positions']].plot(figsize=(10,6), secondary_y='positions')
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))

plt.title('SMA cross over stratergy')
plt.show()


























