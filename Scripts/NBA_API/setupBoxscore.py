import os, sys, pandas as pd, configparser
from classes.boxScore import boxScore

'''
This code setups the boxscore object and calculates some advanced stats that you might be interested in.
argv[1]: dataDir-the directory of data that you want to read in
argv[2]: outputDir-the directory where you want to save the final boxscore

Run as: python3 setupBoxscore.py dailyConfig.config
'''

# read in the config file
configFile = sys.argv[1]
config = configparser.ConfigParser()
config.read(configFile)
programName = 'setupBoxscore'
dataDir = config[programName]['dataDir']
outputDir = config[programName]['boxscoreDir']

# make the output directory if it doesn't exist
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# loop through the files in the data directory
for datafile in os.listdir(dataDir):
    # get the name of the datafile without the extension
    filename = datafile.split('.')[0]

    # get the file path
    datafile = os.path.join(dataDir, datafile)

    # initialize the boxscore object
    box = boxScore()

    # set the boxscore
    box.setBoxScore(datafile)

    # sort the boxscore by points
    box.sortBoxScore('PTS')

    # rename the MIN column to MNT
    #box.box = box.box.rename(columns={'MIN':'MNT'})

    # get some advanced stats
    box.statDivision('FGM', 'FGA', 'FG%') # add the field goal percentage column
    box.statDivision('FTM', 'FTA', 'FT%') # add the free throw percentage column
    box.statDivision('FG3M', 'FG3A', '3P%') # add the 3 point percentage column
    box.statDivision('AST', 'TOV', 'AST_TO') # add the assist to turnover ratio column
    # add usage here eventually
    #box.calcUsage()

    # get per game stats
    box.statDivision('PTS', 'GP', 'PPG') # add the points per game column
    box.statDivision('REB', 'GP', 'RPG') # get the turnovers per game
    box.statSubtraction('FGA', 'FG3A', '2PA') # get the number of 2 point field goals attempted per game
    box.statSubtraction('FGM', 'FG3M', '2PM') # get the number of 2 point field goals made per game
    box.statSubtraction('FG3A', 'FGA', '3PA') # get the number of 3 point field goals attempted per game
    box.statDivision('2PM', '2PA', '2P%') # add the 2pt percentage column
    box.statDivision('AST', 'GP', 'APG') # add the assists per game column
    box.statDivision('STL', 'GP', 'SPG') # get the steals per game column
    box.statDivision('BLK', 'GP', 'BPG') # get the blocks per game column
    box.statDivision('OREB', 'GP', 'OREB_PG') # get the turnovers per game
    box.statDivision('DREB', 'GP', 'DREB_PG') # get the turnovers per game
    box.statDivision('FGA', 'GP', 'FGA_PG') # get the number of fg attempts per game
    box.statDivision('FTA', 'GP', 'FTA_PG') # get the number of free throw attempts per game
    box.statDivision('2PM', 'GP', '2PM_PG') # add the 2pt made per game column
    box.statDivision('2PA', 'GP', '2PA_PG') # add the 2pt attempts per game column
    box.statDivision('FG3M', 'GP', '3PM_PG') # add the 3pm per game column
    box.statDivision('FG3A', 'GP', '3PA_PG') # add the 3pa per game column
    box.statDivision('TOV', 'GP', 'TOV_PG') # get the turnovers per game column
    box.statDivision('PF', 'GP', 'PF_PG') # get the turnovers per game column

    # add in minutes per game
    box.statDivision('MIN', 'GP', 'MPG') # add the minutes per game column
    box.convertMinutes('MIN', 'GP', 'clock') # add the minutes per game column

    # temporary until you make your own fantasy points calculation
    box.statDivision('NBA_FANTASY_PTS', 'GP', 'NBA_FANTASY_PTS_PG') # get the fantasy points per game column

    colNames = ['PLAYER_NAME',
    'AGE',
    'TEAM_ABBREVIATION',
    'GP',
    'MPG',
    'clock',
    'FG%',
    'FT%',
    '3P%',
    'PPG',
    'RPG',
    'APG',
    'AST_TO',
    'SPG',
    'BPG',
    'OREB_PG',
    'DREB_PG',
    'TOV_PG',
    'PF_PG',
    'FGA_PG',
    'FTA_PG',
    '3PA_PG',
    '3PM_PG',
    '2PA_PG',
    '2PM_PG',
    '2P%',
    'NBA_FANTASY_PTS_PG']

    finalBox = box.extractBoxScoreColumns(colNames)

    # save the final boxscore to a csv file
    finalBox.to_csv(f'{outputDir}/{filename}_boxscore.csv', index=False)