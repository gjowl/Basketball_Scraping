import os, sys
import pandas as pd
from classes.boxScore import boxScore
from classes.teamScore import teamScore

# read in the input data from the command line
dataFile = sys.argv[1]

# read in the data as a pandas dataframe
df = pd.read_csv(dataFile)

# initialize the boxscore object
box = boxScore()

# set the boxscore
box.setBoxScore(dataFile)

# add the points per game column
box.statDivision('PTS', 'GP', 'PPG')

# add the assist to turnover ratio column
box.statDivision('AST', 'TOV', 'AST/TO')

# add the 3pm per game column
box.statDivision('FG3M', 'GP', '3PM/G')

# sort the boxscore by points per game
box.sortBoxScore('PPG')

# only keep the columns we want
df = box.extractBoxScoreColumns(['PLAYER_NAME', 'PPG', 'AST/TO', '3PM/G'])

# print the top 10 players in points per game without the index
miaScore = box.getTeamScore('MIA')
print(miaScore.getBoxScore())



# TODO: find value players (50, 40, 75? 50, 35, 80? maybe depending on usage rate? how many of those guys are on playoff teams?, non-playoff teams?, 
# championship teams?, non-championship teams?)

## TODO: choose what stats to search for; assist to turnover ratio, 3pms, triple doubles, etc.
## define the points per game column
#df['PPG'] = df['PTS'] / df['GP']
## define the assist to turnover ratio column
#df['AST/TO'] = df['AST'] / df['TOV']
#df = df.sort_values(by=['PPG'], ascending=False)
#ppgDf = df.head(10)
#
## loop through the 
#for index, row in ppgDf.iterrows():
#    # print the player name and ppg
#    print(f'{row['PLAYER']} | {row['PPG']}\n')
#
## find the players with the highest assist to turnover ratio
#df = df.sort_values(by=['AST/TO'], ascending=False)
#astDf = df.head(10)
## find the players with the highest 3pms
#df = df.sort_values(by=['3PM'], ascending=False)
#threeDf = df.head(10)
## add the dataframes to a list
#dfs = [ppgDf, astDf, threeDf]
#
#