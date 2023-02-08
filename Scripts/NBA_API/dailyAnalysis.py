import os, sys
import pandas as pd
from classes.boxScore import boxScore

# get the current working directory
# TODO: in the future, change this to something else
cwd = os.getcwd()

# read in the input data from the command line
dataFile = sys.argv[1]

# read in the data as a pandas dataframe
df = pd.read_csv(dataFile)

# initialize the boxscore object
box = boxScore()

# set the boxscore
box.setBoxScore(dataFile)

# TODO: how to decide what stats to output? maybe just the top for each on the ticker? Or add these to a list, shuffle them to a ticker, etc.?
# or like a rolling ticker up and down on different parts of the page? like the top 5 players in each stat
box.calcUsage()
print(box.getBoxScore())
# print the top 10 players in points per game without the index
#miaScore = box.getTeamBoxScore('MIA')
#print(miaScore.getBoxScore())

# add the points per game column
box.statDivision('PTS', 'GP', 'PPG')

# add the assist to turnover ratio column
box.statDivision('AST', 'TOV', 'AST/TO')

# add the 3pm per game column
box.statDivision('FG3M', 'GP', '3PM/G')

# add the minutes per game column
box.statDivision('MIN', 'GP', 'MIN/G')

# sort the boxscore by points per game
box.sortBoxScore('PPG')

# only keep the columns we want
df = box.extractBoxScoreColumns(['PLAYER_NAME', 'TEAM_ABBREVIATION', 'MIN/G', 'PPG', 'AST/TO', '3PM/G', 'USG%'])
# sort by usage rate
df = df.sort_values(by=['3PM/G'], ascending=False)
print(df)

# save the dataframe to a csv file
df.to_csv(cwd+'/advancedBoxScore.csv', index=False)



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