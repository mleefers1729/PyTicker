import ticker
with open('polygonKey.txt','r') as f:
    lines = f.readlines()
    myKey = lines[0]
f.close()
assetDict = {}

sel = input("Would you like to add an asset to analyze? (y or n)")
if sel.lower() == 'y':
    asset = input("Enter a stock Ticker:")
    name = input("What'll ya call it? ")
    newTicker = ticker.polyAsset(asset,myKey)
    newTicker.setName(name)
    assetDict[newTicker.name] = newTicker
    interval = input('What interval do you wanna look at? (Your optionios are: hour,minute,day) ')
    multiplier = input("Do you wanna look at a single interval or multiple togeter? (ex: if you said 'hour' above and you say 4 here, you'll et 4 hour bars) ")
    start = input("Enter the start time (YYYY-MM-DD HH:mm)")
    end = input("Enter the end time (YYYY-MM-DD HH:mm)")

    data = newTicker.getAggregatedBars(interval,multiplier,start,end)
    trend = newTicker.getTrendDirection(data)
    print(trend[0])
    print(trend[1])
else:
    exit(1)
# for r in test['results']:
#     r['t'] = ticker.getNiceTime(int(r['t']))
#     print(r)