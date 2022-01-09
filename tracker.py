import requests
import json
import time

names = [
'player1',
'player2',
'player3'
]

key = 'API Key' # set this to your api key [/api new]
webhook = 'Webhook' # set this to your webhook url
delay = 10



print("Starting")
data = {
    "content" : """```ini
[Starting tracker...]```"""
}
result = requests.post(webhook, json = data)

while True:
    for player in names:
        
        time.sleep(1) # fixes error from spamming hypixel api
        print(f"Checking {player}")
        try:
            getuuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}').json()
            unformatteduuid = getuuid['id']
        except:
            print(f"{player} doesn't seem to exist! Douple check your spelling.")
        a = []
        for letter in unformatteduuid:
            a += letter
        uuid = a[0]+a[1]+a[2]+a[3]+a[4]+a[5]+a[6]+a[7]+'-'+a[8]+a[9]+a[10]+a[11]+'-'+a[12]+a[13]+a[14]+a[15]+'-'+a[16]+a[17]+a[18]+a[19]+'-'+a[20]+a[21]+a[22]+a[23]+a[24]+a[25]+a[26]+a[27]+a[28]+a[29]+a[30]+a[31]
        params = {'api': key}

        overallstats = requests.get(f'https://api.voxyl.net/player/stats/overall/{uuid}', params=params).json()
        level = overallstats['level']
        
        gamestats = requests.get(f'https://api.voxyl.net/player/stats/game/{uuid}', params=params).json()
        
        stored = False
        try:
            betasumo = gamestats['stats']['betaSumo']['kills']
        except:
            betasumo = '0'
        try:
            stick = gamestats['stats']['stickFightSingle']['kills']
        except:
            stick = '0'
        try:
            flat = gamestats['stats']['flatFightSingle']['kills']
        except:
            flat = '0'
        try:
            bow = gamestats['stats']['bowFightSingle']['kills']
        except:
            bow = '0'
        try:
            bridges = gamestats['stats']['bridgesSingle']['kills']
        except:
            bridges = '0'
        try:
            pearl = gamestats['stats']['pearlFightSingle']['kills']
        except:
            pearl = '0'
        try:
            void = gamestats['stats']['voidSingle']['kills']
        except:
            void = '0'
        try:
            bedrush = gamestats['stats']['bedRushSingle']['kills']
        except:
            bedrush = '0'
        try:
            resource = gamestats['stats']['resourceSingle']['kills']
        except:
            resource = '0'
        try:
            sumo = gamestats['stats']['sumo']['kills']
        except:
            sumo = '0'
        try: # check if player is stored
            datafile = open(f'./data/{player}.json', 'r')
            datafile.close()
            try: # gets old stats
                datafile = open(f'./data/{player}.json', 'r')
                data = json.load(datafile)
                datafile.close()
            
                oldbetasumo = data[player]['betasumo']
                oldstick = data[player]['stick']
                oldflat = data[player]['flat']
                oldbow = data[player]['bow']
                oldbridges = data[player]['bridges']
                oldpearl = data[player]['pearl']
                oldvoid = data[player]['void']
                oldbedrush = data[player]['bedrush']
                oldresource = data[player]['resource']
                oldsumo = data[player]['sumo']
                stored = True
            except:
                pass
            
        except: # if player not stored > creates file
            datafile = open(f'./data/{player}.json', 'w')
            dump = {player:{"betasumo":betasumo,"stick":stick,"flat":flat,"bow":bow,"bridges":bridges,"pearl":pearl,"void":void,"bedrush":bedrush,"resource":resource,"sumo":sumo}}
            json.dump(dump, datafile)
            datafile.close()
            print(f"Adding {player} to database.")
            
            
            datafile.close()
            stored = False
        send = False
        if stored: # if player was stored > overrides data
        
            # checks if mode stats changed
            if int(betasumo) > int(oldbetasumo): 
                mode = 'Beta Sumo'
                send = True
            elif int(stick) > int(oldstick):
                mode = 'Stick Fight'
                send = True
            elif int(flat) > int(oldflat):
                mode = 'Flat Fight'
                send = True
            elif int(bow) > int(oldbow):
                mode = 'Bow Fight'
                send = True
            elif int(bridges) > int(oldbridges):
                mode = 'Bridges'
                send = True
            elif int(pearl) > int(oldpearl):
                mode = 'Pearl Fight'
                send = True
            elif int(void) > int(oldvoid):
                mode = 'Void Fight'
                send = True
            elif int(bedrush) > int(oldbedrush):
                mode = 'Bed Rush'
                send = True
            elif int(resource) > int(oldresource):
                mode = 'Resource Collect'
                send = True
            elif int(sumo) > int(oldsumo):
                mode = 'Sumo'
                send = True
            datafile = open(f'./data/{player}.json', 'w')
            dump = {player:{"betasumo":betasumo,"stick":stick,"flat":flat,"bow":bow,"bridges":bridges,"pearl":pearl,"void":void,"bedrush":bedrush,"resource":resource,"sumo":sumo}}
            json.dump(dump, datafile)
            datafile.close()
            if send: # webhook send
                data = {
                "content" : f"""```css
[({level}⭐) {player} is playing {mode}]```"""
                    }
                result = requests.post(webhook, json = data)
    print(f"Finished checking {len(names)} players! Sleeping {delay} seconds.\n-----\n")
    time.sleep(delay)
