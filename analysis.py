import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from nsepy import get_history
from datetime import datetime as dt 

start_date = dt(2000,1,1)
end_date = dt.now()


df = get_history("Nifty",start_date,end_date,index=True)

print(df.head())

df.to_csv("Nifty50.csv")



