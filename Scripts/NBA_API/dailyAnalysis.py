import os, sys
import pandas as pd

# read in the input data from the command line
dataFile = sys.argv[1]

# read in the data as a pandas dataframe
df = pd.read_csv(dataFile)

# TODO: choose what stats to search for; assist to turnover ratio, 3pms, triple doubles, etc.
# define the points per game column
df['PPG'] = df['PTS'] / df['GP']
# define the assist to turnover ratio column
df['AST/TO'] = df['AST'] / df['TOV']
df = df.sort_values(by=['PPG'], ascending=False)
ppgDf = df.head(10)

# 

# find the players with the highest assist to turnover ratio
df = df.sort_values(by=['AST/TO'], ascending=False)
astDf = df.head(10)

# find the players with the highest 3pms
df = df.sort_values(by=['3PM'], ascending=False)
threeDf = df.head(10)

# add the dataframes to a list
dfs = [ppgDf, astDf, threeDf]