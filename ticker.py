import requests
from datetime import datetime
import pandas as pd

# Utility functions used for universal analysis of price and indicators
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

def getTrendDirection(data,trendType):
        if trendType == 'price':
            ds = pd.DataFrame(data['results'],index=[x['t'] for x in data['results']])
            valLst = ds['l'].to_list()
            chngLimit = 0.25
        else:
            ds = pd.DataFrame(data['results']['values'])
            times = ds['timestamp'].to_list()
            humanTimes = [getNiceTime(int(t)) for t in times]
            ds.insert(1,'Date',humanTimes)
            ds.sort_values(by='timestamp', ascending=True, inplace=True)
            valLst = ds['value'].to_list()
            chngLimit = 10
        
        v1 = valLst[0]
        trend = valLst[-1] - v1
        percChange = ((valLst[-1]-v1)/v1) * 100

        if percChange > chngLimit:
            return {'direction':"Trending Up",'value':percChange}
        elif percChange < -chngLimit:
            return {'direction':"Trending Down", 'value':percChange}
        else:
            return {'direction':"Moving Sideways", 'value':percChange}

# The main class that is implemented for tracking assets
class polyAsset:
    def __init__(self,ticker,apiKey):
        self.apiKey = apiKey
        self.ticker = ticker.upper()
        self.name = ''
        self.baseURL_1 = 'https://api.polygon.io/v1/'
        self.baseURL_2 = 'https://api.polygon.io/v2/'
        self.rsiTrend = 0
        self.priceTrend = 0

    # defining setter functions here
    def setName(self,name):
        self.name = name
    
    def setKey(self,apiKey):
        self.apiKey = apiKey
    
    def setRsiTrend(self,value):
        self.rsiTrend = value
   
    def setPriceTrend(self,value):
        self.priceTrend = value
    
    # defining analysis functions for an asset object
    
    def getAggregatedBars(self,interval,multiplier,start,end):
        start = getMiliTime(start)
        end = getMiliTime(end)
        URL = self.baseURL_2 + "aggs/ticker/" + self.ticker + "/range/" + str(multiplier) + "/" + interval.lower() + "/" + str(int(start)) + "/" + str(int(end))
        URL = URL + "?adjusted=true&sort=asc&limit=5000&apiKey=" + self.apiKey
        result = requests.get(URL,params = {}).json()
        trend = getTrendDirection(result,'price')
        self.priceTrend = trend['value']
        return result
    

    def getRsiData(self,interval,start,end,window=14,limit=5000):
        start = int(getMiliTime(start))
        end = int(getMiliTime(end))
        URL = self.baseURL_1 + "indicators/rsi/" + self.ticker + "?timestamp.gte=" + str(start)
        URL = URL + "&timestamp.lte=" + str(end) + "&timespan=" + interval.lower()  
        URL = URL + "&adjusted=true&window=" + str(window) + "&series_type=close&order=desc&limit=" + str(limit) + "&apiKey=" + self.apiKey
        result = requests.get(URL,params = {}).json()
        trend = getTrendDirection(result,'rsi')
        self.rsiTrend = trend['value']
        return result
    
    def findRsiDivergences(self):
        if self.rsiTrend > 5 and self.priceTrend < -0.25:
            return("Strong BULLISH RSI divergence found")
        elif self.rsiTrend < 5 and self.priceTrend > -0.25:
            return("Strong BEARISH RSI divergence found")
        elif self.rsiTrend > 0 and (-0.25 < self.priceTrend < 0.25):
            return("Medium BULLISH RSI divergence found")
        elif self.rsiTrend < 0 and (-0.25 > self.priceTrend > 0.25):
            return("Medium BEARISH RSI divergence found")
        elif (-5 < self.rsiTrend < 5) and self.priceTrend < -0.25:
            return("Weak BULLISH RSI divergence found")
        elif (-5 > self.rsiTrend > 5) and self.priceTrend > -0.25:
            return("Weak BEARISH RSI divergence found")
        elif self.rsiTrend < 5 and self.priceTrend > 0.25:
            return("Hidden BULLISH RSI divergence found")
        elif self.rsiTrend > 5 and self.priceTrend < 0.25:
            return("Hidden BEARISH RSI divergence found")