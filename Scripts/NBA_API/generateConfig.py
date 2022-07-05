"""
Example code for generating a configuration file for NBA statistics scraper
"""
import os
import configparser

# create config file object
config_file = configparser.ConfigParser()

# set up directory structure
currDir = os.getcwd()
parentDir = os.path.dirname(currDir)

# main code config options
programName = 'NBA_API'
requirementsFile = currDir + "requirements.txt"

# input config options
# set value as null
starter_bench = None # 'Starters' or 'Bench'
draft_year = None # year drafted: 1947 to current year
draft_pick = None # 1st Round, 2nd Round, Lottery Pick, Undrafted
outcome = None # 'Wins' or 'Losses'
shot_clock_range = None # default is any shot clock range: 24-22, 22-18 Very Early, 18-15 Early, 15-7 Average, 7-4 Late, 4-0 Very Late
season_type = 'Regular+Season' # 'Regular+Season', 'Playoffs', 'Preseason'; likely eventually 'Playin' and 'In+Season+Tournament'
season_list = ['2019-20', '2020-21'] # number of seasons to get data for: from x to current season
period = '0' # quarter: 0, 1, 2, 3, 4, 5, 6, 7, 8

# main code section
config_file["main"]={
    'programName':programName,
    'starter_bench':starter_bench,
    'draft_year':draft_year,
    'draft_pick':draft_pick,
    'outcome':outcome,
    'shot_clock_range':shot_clock_range,
    'season_type':season_type,
    'season_list':season_list,
    'period':period
}

# SAVE CONFIG FILE
with open(configFile, 'w+') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

# create the configuration file name based on the variables
configName = f"SB{starter_bench}_DY{draft_year}_DP{draft_pick}_O{outcome}_SCR{shot_clock_range}_ST{season_type}_SL{season_list}_P{period}"
print("Config file "+configName+".config created")

# PRINT FILE CONTENT
read_file = open(configFile, "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()