import requests 
import ticker
import pandas as pd
baseURL = 'https://api.polygon.io/v2/'

with open('polygonKey.txt','r') as f:
    lines = f.readlines()
    myKey = lines[0]
f.close()

# asset = input("Enter a stock Ticker Ya wanker:")
# name = input("What'll ya call it dickhead? ")
# print("Very well. Lets move on ass face.")
newTicker = ticker.polyAsset('sq',myKey)
# newTicker.setName(name)
# interval = input('What interval do you wanna look at? (Your optionios are: hour,minute,day) ')
# multiplier = input("Do you wanna look at a single interval or multiple togeter? (ex: if you said 'hour' above and you say 4 here, you'll et 4 hour bars) ")
# start = input("Enter the start time (YYYY-MM-DD HH:mm)")
# end = input("Enter the end time (YYYY-MM-DD HH:mm)")

#test = newTicker.getAggregatedBars('hour',1,'2022-12-07 12:00','2022-12-13 16:00')
# for r in test['results']:
#     r['t'] = ticker.getNiceTime(int(r['t']))
#     print(r)
#ds = pd.DataFrame(test['results'],index=[x['t'] for x in test['results']])
#pLst = ds['l'].to_list()

'''
#These two blocks return the exact same result
trend = pLst[-1] - pLst[0]

for i in range(1,len(pLst)):
    if pLst[i] > pLst[i-1]:
        trend+=(pLst[i] - pLst[i-1])
    else:
        trend-=(pLst[i-1]-pLst[i])
'''

test= newTicker.rsiTrend('hour','',start='2022-12-16 05:00',end='2022-12-19 14:00')
ds = pd.DataFrame(test['results']['values'])
times = ds['timestamp'].to_list()
humanTimes = [ticker.getNiceTime(int(t)) for t in times]
ds.insert(1,'Date',humanTimes)
ds.sort_values(by='timestamp', ascending=True, inplace=True)
print(ds)