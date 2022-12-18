import ticker
with open('polygonKey.txt','r') as f:
    lines = f.readlines()
    myKey = lines[0]
f.close()

asset = input("Enter a stock Ticker Ya wanker:")
name = input("What'll ya call it dickhead? ")
print("Very well. Lets move on ass face.")
newTicker = ticker.polyAsset(asset,myKey)
newTicker.setName(name)
interval = input('What interval do you wanna look at? (Your optionios are: hour,minute,day) ')
multiplier = input("Do you wanna look at a single interval or multiple togeter? (ex: if you said 'hour' above and you say 4 here, you'll et 4 hour bars) ")
start = input("Enter the start time (YYYY-MM-DD HH:mm)")
end = input("Enter the end time (YYYY-MM-DD HH:mm)")

test = newTicker.getAggregatedBars(interval,multiplier,start,end)
for r in test['results']:
    r['t'] = ticker.getNiceTime(int(r['t']))
    print(r)