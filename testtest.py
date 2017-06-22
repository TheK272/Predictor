import requests
import json
import os
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
import pandas as p
import numpy as n
import random
import csv

#target = open("Challenger.csv", 'w')
#target = open("ChalMatchIds.csv", 'r')
target = open("TestMatches2.csv", 'w')

def addPlayers(matchId):
	
	match = riotapi.get_match(matchId, False)
	
	for participant in match.participants:
		
		role = calcRole(participant.timeline.role, participant.timeline.lane)
		tempSTR = str(match.id) + "," + str(participant.summoner_id) + ","+ str(participant.side) + "," + str(participant.previous_season_tier.value) + "," + str(role) + "," + str(participant.champion.name) + "," + str(participant.stats.kills) + "," + str(participant.stats.deaths) + "," + str(participant.stats.assists) + "," + str(participant.stats.gold_earned) + "," + str(participant.stats.win) + "," + str(match.creation) + "\n"
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

def main():
	global countRecor
	
	#constants used to call API
	key = "RGAPI-e445116f-becd-41ea-92a5-847b97546d4b"
	NA = "NA"
	goldSeed = "77179274"
	colinkey = "RGAPI-7532451d-454e-4743-88cb-b687ae5ce5d6"
	joe1key = "RGAPI-a261f6cd-0447-471e-8ddc-6358f6b0fd45"
	joe2key = "RGAPI-f536538b-f908-49b0-a27f-d7a67a779527"

	#set region and key
	riotapi.set_region("NA")
	riotapi.set_api_key(key)
	
	
	with open('ChalMatchIds.csv', 'rb') as f:
		reader = csv.reader(f)
		matches = list(reader)
	
	i = 0
	for ID in matches[0]:
		if i > 3:
			break
		i = i+1
		addPlayers(ID)

	target.close()
	

if __name__ == "__main__":
    main()	