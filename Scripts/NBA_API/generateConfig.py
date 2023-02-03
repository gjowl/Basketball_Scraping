"""
Example code for generating a configuration file for NBA statistics scraper
"""
import os
import configparser
from datetime import datetime

# get current date
date = datetime.today().strftime('%Y-%m-%d')

# create config file object
config_file = configparser.ConfigParser()

# set up directory structure
currDir = os.getcwd() +'/'
parentDir = os.path.dirname(currDir) + '/'

# main code config options
programName = 'regularSeasonDailyPull'
requirementsFile = currDir + "requirements.txt"

# input config options
# set value as null
starter_bench = '' # 'Starters' or 'Bench'
draft_year = '' # year drafted: 1947 to current year
draft_pick = '' # 1st Round, 2nd Round, Lottery Pick, Undrafted
outcome = '' # 'Wins' or 'Losses'
shot_clock_range = '' # default is any shot clock range: 24-22, 22-18 Very Early, 18-15 Early, 15-7 Average, 7-4 Late, 4-0 Very Late
season_type = 'Regular+Season' # 'Regular+Season', 'Playoffs', 'Preseason'; likely eventually 'Playin' and 'In+Season+Tournament'
season_list = '2022-23' # number of seasons to get data for: from x to current season
month = '0' # 0 for all months, 1 for January, 2 for February, etc.
period = '' # quarter: 0, 1, 2, 3, 4, 5, 6, 7, 8

# main code section
config_file[programName]={
    'outputDir': currDir,
    'starter_bench':starter_bench,
    'draft_year':draft_year,
    'draft_pick':draft_pick,
    'outcome':outcome,
    'shot_clock_range':shot_clock_range,
    'season_type':season_type,
    'season_list':season_list,
    'period':period,
    'month':month,
    'requirementsFile':requirementsFile,
    'per_mode_list':'Totals,PerGame,Per36,Per100Possessions,Per100Plays',
    'lastNGames_list':'3,5,7,10,15'
}

configName = programName + '.config'
configFile = currDir + configName
# SAVE CONFIG FILE
with open(configFile, 'w+') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

# create the configuration file name based on the variables
print("Config file "+configName+".config created")

# PRINT FILE CONTENT
read_file = open(configFile, "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()