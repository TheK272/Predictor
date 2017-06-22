import os
import pandas as p
import csv


#input is file data set where a game is 10 lines
#puts a game on one line and replaces stats
#withe the average for each champion


target = open("FinalModelMatches2.csv", 'w')
totInv = 0
avg = p.read_csv('ChampModelAvg.csv')

def oneGame(matchPlayers):

	order = []
	i = 0
	invalid = 0
	while i < 10:
		if invalid > 100:
			global totInv
			totInv = totInv + 1
			return
		for p in matchPlayers:
			if i < 5 and p[2] == "100":
				if p[4] == "top" and i == 0:
					order.append(p)
					i=i+1
				elif p[4] == "jg" and i == 1:
					order.append(p)
					i=i+1
				elif p[4] == "mid" and i == 2:
					order.append(p)
					i=i+1
				elif p[4] == "adc" and i == 3:
					order.append(p)
					i=i+1
				elif p[4] =="sup" and i == 4:
					order.append(p)
					i=i+1
				else:
					invalid = invalid+1
					pass
			elif p[2] == "200":
				if p[4] == "top" and i == 5:
					order.append(p)
					i=i+1
				elif p[4] == "jg" and i == 6:
					order.append(p)
					i=i+1
				elif p[4] == "mid" and i == 7:
					order.append(p)
					i=i+1
				elif p[4] == "adc" and i == 8:
					order.append(p)
					i=i+1
				elif p[4] =="sup" and i == 9:
					order.append(p)
					i=i+1
				else:
					invalid = invalid+1
					pass			
			else:
				pass
	

	#Create csv string for one line in new file
	
	temp = order[0][0]
	for p in order:
		champRole = avg[(avg['role'] == order[0][4])&(avg['champion'] == order[0][5])].dropna()
		temp = temp + "," + str(champRole.iloc[0]['kills']) + "," + str(champRole.iloc[0]['deaths']) + "," + str(champRole.iloc[0]['assists']) + "," + str(champRole.iloc[0]['gold']) + "," + str(champRole.iloc[0]['win'])
	
	
	if order[0][10] == "TRUE":
		temp = temp +"," + "1" + "\n"
	else:
		temp = temp +"," + "2" + "\n"

	#write line to file
	target.write(temp)


def main():

	#Read match file
	f = csv.reader(open("FinalModelData.csv"), delimiter=",")

	#Add 10 players from game to a list
	total = 0
	count = 0
	while True:
		matchPlayers = []
		total = total+1
		if total%10000 == 0:
			print total
			print totInv
		while count < 10:
			matchPlayers.append(f.next())
			count= count+1
		oneGame(matchPlayers)
		count = 0
	
	
	target.close()
	
	

if __name__ == "__main__":
    main()	