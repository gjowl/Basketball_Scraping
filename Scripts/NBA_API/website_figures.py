import os, sys, pandas as pd, numpy as np
import time
import matplotlib.pyplot as plt
from classes.boxScore import boxScore

'''
This code setups the boxscore object and calculates some advanced stats that you might be interested in.

Run as: python3 graphData.py
'''

# read in the data file from command line
dataFile = sys.argv[1]
#dataFile = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD/2023-24.csv'
outputDir = sys.argv[2]

# if outputDir doesn't exist, create it
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# Functions
def wait(number):
    time.sleep(number)

if __name__ == '__main__':
    # read in the data as a pandas dataframe
    df = pd.read_csv(dataFile)

    # initialize the boxscore object
    box = boxScore()

    # set the boxscore
    box.setBoxScore(dataFile)

    # TODO:
    # 1. Percentiles: If the PPG category is clicked, show the percentiles for each player in the league. Compare scoring by other seasons
    # 2. Under that have it so that if you hover over a percentile (it shows the top 5-10 players in this percentile) with faces, ppg, and a total points (if possible)
    # 3. Do this for all games and the last n games as well

    # To start, just work with the 2023-2024 season data

    # get the average points per game for the top 10 players in the league
    df_top = df.sort_values(by='PPG', ascending=False).head(10)
    print(df_top)
    avgPPG = df_top['PPG'].mean()
    avgPPG = round(avgPPG, 3)
    minPPG = df_top['PPG'].min()

    # count the total number of players in the league (games played minimum 25)
    df = df[df['GP'] >= 25]
    numPlayers = df['PLAYER_NAME'].count()

    # calculate the percentiles for the PPG column
    df['PPG_Percentile'] = df['PPG'].rank(pct=True)
    df['PPG_Percentile'] = df['PPG_Percentile'].round(3)

    # top 10 players in the league percentiles
    minPlayerDf = df[df['PPG'] > minPPG]
    min_num_players = minPlayerDf['PLAYER_NAME'].count()
    min_percentile = min_num_players/numPlayers*100
    min_percentile = round(min_percentile, 3)
    print(f'The average PPG for the top 10 players in the league is {avgPPG}')
    print(f'The minimum PPG for the top 10 players in the league is {minPPG}')
    print(f'The average PPG for the league is {df["PPG"].mean()}')
    print(f'The minimum PPG for the league is {df["PPG"].min()}')
    print(f'The number of players in the league (min 25 GP) is {numPlayers}')
    print(f'The top 10 players by minimum is in the {min_percentile} percentile')
