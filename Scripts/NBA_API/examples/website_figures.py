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
outputDir = sys.argv[2]

# Functions
def wait(number):
    time.sleep(number)

if __name__ == '__main__':
    # wait for 1 minute to let the first program finish running (in case these and the data fetching script are run parallel; I should probably figure out if that's true?)
    wait(1)

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