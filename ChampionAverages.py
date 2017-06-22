import pandas as p
import csv

#puts game data into pandas dataframe, then sorts by champion and role
#calculates average for each champion in each role

data = p.DataFrame(columns=['matchID', 'rank', 'champion', 'kills', 'deaths', 'assists', 'gold', 'win'])


def main():

	data2 = p.read_csv("AllMatches.csv",  header=None)
	data2.columns = ['matchID', 'playerID', 'team', 'rank', 'role', 'champion', 'kills', 'deaths', 'assists', 'gold', 'win', 'time']
	group = data2.groupby(['champion', 'role'])['kills', 'deaths', 'assists', 'gold', 'win'].mean()
	
	group.to_csv("ChampModelAvg.csv")
	print group	

if __name__ == "__main__":
    main()	