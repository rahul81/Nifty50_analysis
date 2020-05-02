import pandas as pd 
import numpy as np  
import matplotlib.pyplot as plt 
from matplotlib import style 
from datetime import datetime as dt
from nsepy import get_history
import requests
import bs4 as bs
import pickle
import time
import os 

style.use("ggplot")


# Web Scraping 


# Fetching all 50 company's listed in NIFTY50 index tickers from wikipedia page


def get_tickers():

    #getting the webpage of Nifty50 from wikipedia
    data = requests.get("https://en.wikipedia.org/wiki/NIFTY_50")
    soup = bs.BeautifulSoup(data.text, 'lxml')

    #fetching the table structure from html which contains the company names and tickers data
    table = soup.find("table",{"id":"constituents"})
    tickers = []
    
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll("td")[1].text
        ticker = ticker.split(".")[0]
        tickers.append(ticker)

    #saving the fetched and cleaned tickers data to a pickle file for later use
    with open("Nifty50_tickers.pickle",'wb') as f:
        pickle.dump(tickers,f)

    return tickers


# print(get_tickers())



# Fetch stock price data for each ticker listed in Nifty 50 index  


start_date = dt(2000,1,1)

end_date = dt.now()


def get_stock_data():

    #check if scarped ticker dat is already present 

    if os.path.exists('./Nifty50_tickers.pickle'):
        tickers = pickle.load(open("Nifty50_tickers.pickle",'rb'))
    else:
        tickers = get_tickers()

    # for each ticker in list tickers pull stock data from start date to end date

    for i,ticker in enumerate(tickers) :

        if os.path.exists("./data/"+ticker+".csv"):
            print(ticker + " Already present")
        else:
            print("Getting stock data of "+ ticker)
            time.sleep(30)
            df = get_history(ticker,start_date,end_date)
            df.to_csv("./data/"+ticker+".csv")
            print(f"Remaining tickers {50-i+1}")
            


#optimize dataframe for less memory consumption and faster computation

def type_conversion(pds_obj):
    
    optimized_obj = pds_obj.copy()
    
    #selecting all columns with integer datatype
    int_col = pds_obj.select_dtypes(include=['int64'])
    if len(int_col.columns)==0:
        pass
    else:
        new_int = int_col.apply(pd.to_numeric,downcast='unsigned')
        optimized_obj[int_col.columns] = new_int
    
    #selecting all columns with float datatype
    float_col = pds_obj.select_dtypes('float')
    if len(float_col.columns)==0:
        pass
    else:
        new_float = float_col.apply(pd.to_numeric,downcast='float')
        optimized_obj[float_col.columns] = new_float
    #selecting all columns with object datatype
    objects = pds_obj.select_dtypes('object').copy()
    if len(objects.columns)==0:
        pass
    else:
        obj =objects.astype('category')
        optimized_obj[objects.columns]=obj
    

    return optimized_obj
    

    
    
# function to combine closing price for all 50 tickers in one file

def combine_data(): 

    tickers = pickle.load(open("./Nifty50_tickers.pickle",'rb'))

    #initialize an empty dataframe which will hold all the combined data
    all_data = pd.DataFrame()

    # for each ticker read it's csv file, get the closing price and add it to the all_data dataframe 

    for i,ticker in enumerate(tickers): 
        df = pd.read_csv("./data/"+ticker+".csv")
        df.rename(columns={'Close':ticker},inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index(['Date'],inplace=True)

        df = df.drop(['Symbol','Series','Prev Close','Open','High','Low','Last','VWAP','Volume','Turnover','Trades','Deliverable Volume',"%Deliverble"],axis=1)
        print(df)
        
        if all_data.empty:
            all_data=df
        else: 
            all_data = all_data.join(df,how='outer')
            all_data = type_conversion(all_data)
            all_data.drop_duplicates(inplace=True)

        if i % 5 ==0:
            print(i)

    
    print(all_data.head())
    print(all_data.shape)
    print(all_data.info(memory_usage='deep'))
    print(len(set(all_data.index)))

    all_data.to_csv("Nifty50_combined.csv")



get_stock_data()

combine_data()











