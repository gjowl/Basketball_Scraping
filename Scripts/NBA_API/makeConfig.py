'''
This file makes the config file for the scraper_withConfig.py script. It is run as: python3 makeConfig.py
'''

import configparser, datetime

# create a ConfigParser object
config = configparser.ConfigParser()

# global variables
mainDir = 'H:/NBA_API_DATA'

# set the values for the scraper script 
config['scraper'] = {
    'mainDir': f'{mainDir}/RAW',
    'season': '2024-25',
    'lastNGames': '0,1,5,10,15,20,25,30',
    'season_type': 'Regular+Season',
    'month': '0',
    'starter_bench': '',
    'draft_year': '',
    'draft_pick': '',
    'outcome': '',
    'shot_clock_range': '',
    'period': '',
    'segment': '',
}

# get the date
date = datetime.datetime.now().strftime("%Y-%m-%d")
dirToAnalyze = 'Totals'
# set the values for the setupBoxscore script
config['setupBoxscore'] = {
    'dataDir': f'{mainDir}/RAW/{config["scraper"]["season"]}/{date}/{dirToAnalyze}',
    'boxscoreDir': f'{mainDir}/BOXSCORES/{date}',
}

# set the values for the graphData script
config['graphData'] = {
    'dataDir': f'{mainDir}/BOXSCORES/{date}',
    'graphDir': f'{mainDir}/GRAPHS/{date}',
}

# set the values for the fantasyCornerStats script
config['fantasyCornerStats'] = {

}

# set the values for the helperScript script
config['helperScript'] = {
    'dataDir': f'{mainDir}/RAW/{config["scraper"]["season"]}/{date}',
}

# write the config file
with open('dailyConfig.config', 'w') as configfile:
    config.write(configfile)