import os
import pandas as p
import csv

#removes 3V3 games from data 

def main():

	data = p.read_csv('AllMatches.csv')
	#Read match file
	f = csv.reader(open("AllMatches.csv"), delimiter=",")
	
	data = p.read_csv('AllMatches.csv', header=None)

	data['freq'] = data.groupby(0)[0].transform('count')

	sort = data.sort_values('freq')
	sort = sort.sort_values(0)
	sort.drop(0, axis=1)
	sort.to_csv('AllMatchesSorted3.csv')

	
if __name__ == "__main__":
    main()