import requests
import json
import os
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
import pandas as p
import numpy as n
import random

matchList = []
usedMatches = []
playerQueue = []
usedPlayers = []
#data = p.DataFrame(columns=['matchID', 'rank', 'champion', 'kills', 'deaths', 'assists', 'gold', 'win'])
target = open("temp.csv", 'w')
countRecor = 0

# function wrapper from cassiopeia library to skip/try again on errors from API

def auto_retry(api_call_method):
    """ A decorator to automatically retry 500s (Service Unavailable) and skip 400s (Bad Request) or 404s (Not Found). """
    def call_wrapper(*args, **kwargs):
        try:
            return api_call_method(*args, **kwargs)
        except APIError as error:
		   # Try Again Once
            if error.error_code in [500, 503]:
                try:
                    print("Got a 500, trying again...")
                    return api_call_method(*args, **kwargs)
                except APIError as another_error:
                    if another_error.error_code in [500, 503, 400, 404]:
                        pass
                    else:
                        raise another_error

            # Skip
            elif error.error_code in [400, 404]:
                print("Got a 400 or 404")
                pass				
            # Fatal
            else:
                raise error
    return call_wrapper



#Adds 10 players from given match to the data set
#Parameters are summoner id index of dataframe, and data to add to
	
def addPlayers(matchId):
	global countRecor
	
	#check length of dataframe, end loop if it is long enough
	if countRecor > 20:
		return
	
	match = riotapi.get_match(matchId, False)
	
	getSummonerIds(match)
	
	#i= len(data.index)
	for participant in match.participants:
		tempSTR = str(match.id) + "," + str(participant.previous_season_tier.value) + "," + str(participant.champion.name) + "," + str(participant.stats.kills) + "," + str(participant.stats.deaths) + "," + str(participant.stats.assists) + "," + str(participant.stats.gold_earned) + "," + str(participant.stats.win) + "\n"

		target.write(tempSTR)
	
		#temp = [match.id, participant.previous_season_tier.value, participant.champion.name, 
		#participant.stats.kills, participant.stats.deaths, participant.stats.assists, participant.stats.gold_earned, participant.stats.win]
		#data.loc[i] = temp
		#i = len(data.index)
		countRecor = countRecor + 1
	
	matchList.remove(matchId)
	usedMatches.append(matchId)
	addMatches()
	return True
	
#get all summoner ids from match add to queue if unused,
#otherwise add to used list	
	
def getSummonerIds(match):

	for participant in match.participants:
		id = participant.summoner_id
		if id in playerQueue or id in usedPlayers:
			if id not in usedPlayers:
				usedPlayers.append(id)
		else:
			playerQueue.append(id)
	return True
	
#takes in a summoner Id and returns random match from last 20 games
#if match already exists it looks for one that doesn't
	
def getNewMatch(summoner):
	global countRecor
	
	#check length of dataframe, end loop if it is long enough
	#if countRecor > 29:
	#	countRecor = 0
	#	return
	
	rand = random.randrange(1,20)
	used = True
	
	#get random match
	temp = riotapi.get_match_list(summoner, 1, rand)
	try:
		match = temp[0].match()
	except:
		playerQueue.remove(summoner.id)
		usedPlayers.append(summoner.id)
		print "in except"
		addMatches()
		return True
	
	
	while used == True:
		try:
		#check if match is used
			if match.id not in matchList and match.id not in usedMatches:
				matchList.append(match.id)
				used = False
				playerQueue.remove(summoner.id)
				usedPlayers.append(summoner.id)
				#addPlayers(match.id)
				return matchList
			else:
				#get next match
				rand = rand+1
				temp = riotapi.get_match_list(summoner, 1, rand)
				match = temp[0].match()
		except:
			playerQueue.remove(summoner.id)
			usedPlayers.append(summoner.id)
			print "in second except"
			addMatches()
			return True
	#matchList.append(match.id)
	
	return True

def addMatches():

	#for player in playerQueue:
		#playerObj = riotapi.get_summoner_by_id(player)
		#getNewMatch(playerObj)
	playerObj = riotapi.get_summoner_by_id(playerQueue[0])
	getNewMatch(playerObj)
	return True
	
riotapi.get_match = auto_retry(riotapi.get_match)
riotapi.get_summoner_by_id = auto_retry(riotapi.get_summoner_by_id)
riotapi.get_match_list = auto_retry(riotapi.get_match_list)
	
def main():
	global countRecor
	
	#constants used to call API
	key = "5220dd30-36ee-4150-89ac-5b557dec01c5"
	NA = "NA"
	goldSeed = "62650386"

	#set region and key
	riotapi.set_region("NA")
	riotapi.set_api_key(key)
	
	#startSummoner = riotapi.get_summoner_by_name("thek272")	
	#sneaky = riotapi.get_summoner_by_name("c9sneaky")
	
	#playerQueue.append(startSummoner.id)
	#playerQueue.append(sneaky.id)
	
	#getNewMatch(startSummoner)
	#getNewMatch(sneaky)
	
	#data = addPlayers(matchList[0], data)
	#data = addPlayers(matchList[1], data)
	
	#addMatches()
	
	#used
	#matchList.append(2458831326)
	#addPlayers(2458831326, data)
	
	#using new root games
	matchList.append(2465084666)
	
	#used
	#matchList.append(2465084666)
	#addPlayers(2448220326, data)
	
	#used
	#matchList.append(2465734273)
	temp = 0
	while True:
		addPlayers(matchList[0])
		countRecor = 0
		temp = temp + 1
		print "another iteration"
		if temp > 50000:
			break
	
	
	print matchList
	print usedMatches
	print playerQueue
	print usedPlayers
	#print "about to start second iter  " 
	#print countRecor
	#matchList.append(2426970326)
	#addPlayers(2426970326, data)
	
	#countRecor = 0
	#print "about to start third iter"
	#matchList.append(2148245269\)
	#addPlayers(matchList[0], data)
	
	#matchList.append(2248970326)
	#addPlayers(2248970326, data)
	
	#matchList.append(2448000326)
	#addPlayers(2448000326, data)
	
	target.close()
	
	#data.to_csv("C:/Users/kylew/OneDrive/Documents/CSE482/Project/1000File.csv")
	
	#print data
	#print matchList
	#print playerQueue
	#print usedPlayers

if __name__ == "__main__":
    main()	