import ticker
with open('polygonKey.txt','r') as f:
    lines = f.readlines()
    myKey = lines[0]
f.close()
assetDict = {}

# This portion is for the general set up. This will turn into a UI eventually.
# Mainly just used for testing now
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

    # Grabbing the data for the selected timeperiod and then finding the trend direction 
    # Note that we are only using the lows right now for trend direction
    data = newTicker.getAggregatedBars(interval,multiplier,start,end)
    trend = newTicker.getTrendDirection(data)
    print(trend[0])
    print(trend[1])
else:
    exit(1)