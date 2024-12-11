import os, sys, pandas as pd
from classes.boxScore import boxScore

'''
This code setups the boxscore object and calculates some advanced stats that you might be interested in.
argv[1]: dataFile-the data file that you want to read in
argv[2]: outputDir-the directory where you want to save the final boxscore

Run as: python3 setupBoxscore.py dataFile outputDir
'''

# read in the data file from command line
dataFile = sys.argv[1]
outputDir = sys.argv[2]

# make the output directory if it doesn't exist
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# read in the data as a pandas dataframe
df = pd.read_csv(dataFile)

# initialize the boxscore object
box = boxScore()

# set the boxscore
box.setBoxScore(dataFile)

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
box.statDivision('FGA', 'GP', 'FGA_G') # get the number of fg attempts per game
box.statDivision('FTA', 'GP', 'FTA_G') # get the number of free throw attempts per game
box.statSubtraction('FGA', 'FG3A', '2PA') # get the number of 2 point field goals attempted per game
box.statSubtraction('FGM', 'FG3M', '2PM') # get the number of 2 point field goals made per game
box.statSubtraction('FG3A', 'FGA', '3PA') # get the number of 3 point field goals attempted per game
box.statDivision('2PM', 'GP', '2PM_G') # add the 2pt made per game column
box.statDivision('2PA', 'GP', '2PA_G') # add the 2pt attempts per game column
box.statDivision('2PM', '2PA', '2P%') # add the 2pt percentage column
box.statDivision('FG3M', 'GP', '3PM_G') # add the 3pm per game column
box.statDivision('FG3A', 'GP', '3PA_G') # add the 3pa per game column
box.statDivision('MIN', 'GP', 'MPG') # add the minutes per game column
box.statDivision('AST', 'GP', 'APG') # add the assists per game column
box.statDivision('STL', 'GP', 'SPG') # get the steals per game column
box.statDivision('BLK', 'GP', 'BPG') # get the blocks per game column

colNames = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MPG', 'FG%', 'FT%', '3P%', 'PPG', 'APG', 'SPG', 'BPG', 'AST_TO', 'FGA_G', 'FTA_G', '3PA_G', '3PM_G', '2PA_G', '2PM_G', '2P%']
finalBox = box.extractBoxScoreColumns(colNames)

# save the final boxscore to a csv file
finalBox.to_csv(f'{outputDir}/finalBoxscore.csv', index=False)