import os, sys, pandas as pd, configparser
from classes.boxScore import boxScore

'''
This code setups the boxscore object for advanced stats, removing extra columns.
argv[1]: dataDir-the directory of data that you want to read in
argv[2]: outputDir-the directory where you want to save the final boxscore

Run as: python3 setupAdvancedBoxscore.py setupAdvancedBoxscore.config
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

    # change the name of the MIN column to MPG
    box.box.rename(columns={'MIN': 'MPG'}, inplace=True)
    box.box.rename(columns={'MIN_RANK': 'MPG_RANK'}, inplace=True)

    # rename any columns with _PCT to %
    box.box.rename(columns=lambda x: x.replace('_PCT', '%'), inplace=True)

    # remove any columns with sp_work_ or E_
    box.box.drop(columns=[col for col in box.box.columns if 'sp_work_' in col], inplace=True)
    box.box.drop(columns=[col for col in box.box.columns if 'E_' in col], inplace=True)

    # calculate POSS_PG
    box.statDivision('POSS', 'GP', 'POSS_PG')

    # get the colNames from the box
    colNames = box.box.columns.tolist()
    # remove TEAM_ID
    colNames.remove('PLAYER_ID')
    colNames.remove('TEAM_ID')
    colNames.remove('NICKNAME')

    finalBox = box.extractBoxScoreColumns(colNames)

    # save the final boxscore to a csv file
    finalBox.to_csv(f'{outputDir}/{filename}_boxscore.csv', index=False)