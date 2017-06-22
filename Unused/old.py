import requests
import json
import os
from cassiopeia import riotapi
import pandas as p
import numpy as n
import random

#Returns 10 match Ids from the Summooner ID parameter

def getMatchIDs(region, ID, key):

	#url used to call API
	URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/matchlist/by-summoner/" + ID + "?api_key=" + key

	#turn response into url object
	data = requests.get(URL)
	JSON = data.json()

	#get and return match ID of last 10 games played
	matchIds = [ match['matchId'] for match in JSON['matches'] ]
	matchIDS = matchIds[0:10]
	return matchIDS
	
	
	
def getPlayersFromMatch(region, ID, key):
	
	#url used to call API
	URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/" + str(ID) + "?api_key=" + key
	
	#turn response into url object
	data = requests.get(URL) 
	JSON = data.json()
	
	#test = JSON.read()
	#testJSON = json.loads(test)
	#testPlayers = testJSON['participants']['winner']
	
	players = {}
	#get summoner Ids of all players in match
	#players =  JSON.get('participants').get(stats)
	players = JSON['participants'][0]['stats']
	#players.append()

	
	#os.remove('players.json')
	with open('C:\Users\kylew\OneDrive\Documents\CSE482\Project\players.json', 'w') as outfile:
	
		json.dump(players, outfile)
		
	return players

#Adds 10 players from given match to the data set
#Parameters are summoner id index of dataframe, and data to add to
	
def addPlayers(summoner, data):

	startSummoner = riotapi.get_summoner_by_name(summoner)	
	
	rand = random.randrange(1,20)
	
	test = riotapi.get_match_list(startSummoner, 1, rand)
	match = test[0].match()
	print match.id
	
	i= len(data.index)
	for participant in match.participants:
		temp = [match.id, participant.summoner_id, participant.previous_season_tier.value, participant.champion.name, 
		participant.stats.kills, participant.stats.deaths, participant.stats.assists, participant.stats.gold_earned, participant.stats.win]
		data.loc[i] = temp
		i = len(data.index)
		
	return data
	
	

#Takes a summoner name and returns the corresponding SummonerID
	
def getSummonerID(region, name, key):

		URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + name + "?api_key=" + key

		data = requests.get(URL)
		JSON = data.json()
		Id = JSON[name]['id']
		Id = str(Id)
		
		return Id

def main():

	data = p.DataFrame(columns=['matchID', 'summonerID', 'rank', 'champion', 'kills', 'deaths', 'assists', 'gold', 'win'])
	
	#constants used to call API
	key = "5220dd30-36ee-4150-89ac-5b557dec01c5"
	NA = "NA"
	EU = "EU"
	goldSeed = "62650386"

	#Get summoner ID for thek272
	
	#ID = getSummonerID(NA, "thek272", key)
	#print ID
	
	#get 10 most recent matches
	
	#matchIds = getMatchIDs(NA, ID, key)
	#print matchIds

	#delete file if it exists already, add match ids to file
	
	#os.remove('data.json')
	#with open('C:\Users\kylew\OneDrive\Documents\CSE482\Project\data.json', 'w') as outfile:
	
	#	json.dump(matchIds, outfile)
	
	#set region and key
	riotapi.set_region("NA")
	riotapi.set_api_key(key)
	
	data = addPlayers("thek272", data)
	data = addPlayers("C9Sneaky", data)
	
	print data
	#players = []
	
	#for match in matchIds:
	#	players.append(getPlayersFromMatch(NA, match, key))

	#players.append(getPlayersFromMatch(NA, '2455903526', key))
	#print players
	

if __name__ == "__main__":
    main()	