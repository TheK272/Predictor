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
#playerQueue = []
#target2 = open("playerList.csv")
#target = open("ChallengerMatches.csv", 'w')
target = open("ChalMatchIds500.csv", "w")
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

		#target.write(tempSTR)
	
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
		if id not in playerQueue:
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
				#addPlayers(match.id)
				return matchList
			else:
				#get next match
				rand = rand+1
				temp = riotapi.get_match_list(summoner, 1, rand)
				match = temp[0].match()
		except:
			playerQueue.remove(summoner.id)
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
	goldSeed = "77179274"

	#set region and key
	riotapi.set_region("NA")
	riotapi.set_api_key(key)
	
	#using new root games
	#matchList.append(2466287821)
	
	ray2 = riotapi.get_summoner_by_id(77179274)
	ray = riotapi.get_match_list(ray2, num_matches=200, ) #ranked_queues='RANKED_SOLO_5x5'
	
	import csv
	with open('playerList.csv', 'rb') as f:
		reader = csv.reader(f)
		players = list(reader)
	
	#print players
	
	i = len(players[0])
	j = 0
	print i
	
	for pee in players[0]:
		print j
		j = j+1
		if j >=500:
			break
		poop = riotapi.get_summoner_by_id(pee)
		currentPlayer = riotapi.get_match_list(poop, num_matches=200, )
		for entry in currentPlayer:
			id = entry.id
			if id not in matchList:
				matchList.append(id)
				temp = str(id) + "," + "\n"
				target.write(temp)
	
	#used
	#matchList.append(2465734273)
	temp = 0
	#while True:
		#addPlayers(matchList[0])
		#temp = temp + 1
		#print "another iteration"
		#if temp > 50000:
		#	break
	
	
	#target.close()

if __name__ == "__main__":
    main()	