import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from nsepy import get_history
from datetime import datetime as dt 
from matplotlib import style

style.use("ggplot")

start_date = dt(2000,1,1)
end_date = dt.now()


# df = get_history("Nifty",start_date,end_date,index=True)

# print(df.tail())

# df.to_csv("Nifty50.csv")


df = pd.read_csv("./data/EICHERMOT.csv",parse_dates=True,index_col=0)



df = df.resample('W').mean()
# print(df.head())


fig = plt.figure(figsize=(12,6))
plt.plot(df.index,df['Close'])
plt.xlabel("Year")
plt.ylabel("Price")
plt.title("Eichermotors stock price over the years")
plt.show()

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





