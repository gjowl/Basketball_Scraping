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

# find the players with the highest assist to turnover ratio
df = df.sort_values(by=['AST/TO'], ascending=False)
astDf = df.head(10)

# find the players with the highest 3pms
df = df.sort_values(by=['3PM'], ascending=False)
threeDf = df.head(10)

# add the dataframes to a list
dfs = [ppgDf, astDf, threeDf]
