import requests
import json
import os
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
import pandas as p
import numpy as n
import random
import csv

target = open("TestMatches10-1.csv", 'w')

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

def addPlayers(matchId):
	
	match = riotapi.get_match(matchId, False)
	
	for participant in match.participants:
		
		role = calcRole(participant.timeline.role, participant.timeline.lane)
		tempSTR = str(match.id) + "," + str(participant.summoner_id) + ","+ str(participant.side.value) + "," + str(participant.previous_season_tier.value) + "," + str(participant.timeline.role.value) + "," + str(participant.timeline.lane.value) + "," + str(role) + "," + str(participant.champion.name) + "," + str(participant.stats.kills) + "," + str(participant.stats.deaths) + "," + str(participant.stats.assists) + "," + str(participant.stats.gold_earned) + "," + str(participant.stats.win) + "," + str(match.creation) + "\n"
		#ADD TEAM ID WHEN COLLECTING GAMES AND BE COMPLETELY SURE u HAVE ALL THE DATA U WANT
		
		target.write(tempSTR)
	
	return True

def calcRole(role, lane):
	pos=""	
	if role.value == "NONE":
		pos = "jg"
	elif role.value == "DUO_SUPPORT":
		pos = "sup"
	elif role.value == "DUO_CARRY":
		pos = "adc"
	else:
		if lane.value == "TOP":
			pos = "top"
		else:
			pos = "mid"
	return pos

	
riotapi.get_match = auto_retry(riotapi.get_match)	
	
def main():

	#constants used to call API
	key = "5220dd30-36ee-4150-89ac-5b557dec01c5"

	#set region and key
	riotapi.set_region("NA")
	riotapi.set_api_key(key)
	
		
	matches = p.read_csv('new 1.csv', header=None)	
	matches = matches[0]
	
	i = 0
	for ID in matches:
		if i > 300:
			break
		i = i+1
		print i
		addPlayers(ID)
	
	target.close()
	
	#chal = riotapi.get_challenger()
	#master = riotapi.get_master()
	#print matchList
		
	#for m in matchList:
		#addPlayers(m)
	
	#target.write(chal)
	
	#challenger = riotapi.get_challenger()
	#for entry in challenger:
	#	temp = str(entry.summoner.id) + ","
	#	target.write(temp)
	
	#for entry in master:
	#	temp = str(entry.summoner.id) + ","
	#	target.write(temp)
	

if __name__ == "__main__":
    main()	