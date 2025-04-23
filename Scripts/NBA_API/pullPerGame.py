import os, datetime, sys, configparser, time
import requests, random
import pandas as pd
from largePullRequest import getDataframeFromWeb, makeOutputDir

file = open(r'D:\github\Basketball_Scraping\Scripts\NBA_API\autoScriptRun.txt', 'a')
file.write(f'Program started at: {datetime.datetime.now()}\n')

# read in the config file
configFile = sys.argv[1]
config = configparser.ConfigParser()
config.read(configFile)
programName = 'scraper'

# config file options below
mainDir = config[programName]['mainDir']
seasons = config[programName]['season'].split(',') # this is a list of seasons, so it can be used to get data for multiple seasons at once
lastNGames = config[programName]['lastNGames']
starter_bench = config[programName]['starter_bench']
draft_year = config[programName]['draft_year']
draft_pick = config[programName]['draft_pick']
outcome = config[programName]['outcome']
season_type = config[programName]['season_type']
period = config[programName]['period']
month = config[programName]['month']
shot_clock_range = config[programName]['shot_clock_range']
segment = config[programName]['segment']
measureType = config[programName]['measureType']

# get the date in month-day-year format using datetime
date = datetime.datetime.now().strftime("%Y-%m-%d")

# hardcoded spot for data to be saved
outputDir = mainDir

# setup the parameters for the getDataframeFromWeb function
parameters = {
    "starter_bench": starter_bench,
    "draft_year": draft_year,
    "draft_pick": draft_pick,
    "outcome": outcome,
    "season_type": season_type,
    "period": period,
    "shot_clock_range": shot_clock_range,
    "month": month,
    "segment": segment,
    'measureType': measureType,
}
# make it so that I get individual draft stats, separated in dataframes, for anyone in the first 4 years of their career

mode = "PerGame"
file.write(f'scraping mode:: {mode}\n')
output = os.path.join(outputDir, mode)
makeOutputDir(output) 
# loop through the lastNGames
for season in seasons:
    file.write(f' - scraping season:: {season}\n')
    # scrape
    nba_df = getDataframeFromWeb(mode, lastNGames, season, parameters)
    # define the file name for the data
    filename = os.path.join(output, f'{season}.csv')
    file.write(filename)
    # save the nba_df to a csv file
    nba_df.to_csv(filename, index=False)

file.write(f'Files saved to: {outputDir}\n')