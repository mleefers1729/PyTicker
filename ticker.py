import requests
from datetime import datetime
import pandas as pd

# Utility functions for converting timestamps
def getMiliTime(t_stamp):
    try:
        dt_obj = datetime.strptime(t_stamp, "%Y-%m-%d %H:%M")
        return dt_obj.timestamp()*1000
    except:
        return None
def getNiceTime(ms_time):
    try:
        t_stamp = datetime.fromtimestamp(ms_time/1000)
        return datetime.strftime(t_stamp,"%Y-%m-%d %H:%M")
    except:
        return None

# The main class that is implemented for tracking assets
class polyAsset:
    def __init__(self,ticker,apiKey):
        self.apiKey = apiKey
        self.ticker = ticker.upper()
        self.name = ''
        self.baseURL = 'https://api.polygon.io/v2/'

    def getAggregatedBars(self,interval,multiplier,start,end):
        start = getMiliTime(start)
        end = getMiliTime(end)
        URL = self.baseURL + "aggs/ticker/" + self.ticker + "/range/" + str(multiplier) + "/" + interval.lower() + "/" + str(int(start)) + "/" + str(int(end))
        URL = URL + "?adjusted=true&sort=asc&limit=5000&apiKey=" + self.apiKey
        result = requests.get(URL,params = {})
        return result.json()
    
    def getTrendDirection(self,data):
        ds = pd.DataFrame(data['results'],index=[x['t'] for x in data['results']])
        priceLst = ds['l'].to_list()
        v1 = priceLst[0]
        trend = priceLst[-1] - v1
        percChange = ((priceLst[-1]-v1)/v1) * 100
        if percChange > 0.25:
            return ["Trending Up",percChange]
        elif percChange < -0.25:
            return ["Trending Down", percChange]
        else:
            return ["Moving Sideways", percChange]

    def setName(self,name):
        self.name = name
    
    def setKey(self,apiKey):
        self.apiKey = apiKey