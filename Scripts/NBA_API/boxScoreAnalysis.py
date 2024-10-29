import os, sys, pandas as pd
import pandas as pd
from classes.boxScore import boxScore

# read in the data file from command line
dataFile = sys.argv[1]

# read in the data as a pandas dataframe
df = pd.read_csv(dataFile)

# initialize the boxscore object
box = boxScore()

# set the boxscore
box.setBoxScore(dataFile)

# calculate the usage rate
box.calcUsage()

# add the points per game column
box.statDivision('PTS', 'GP', 'PPG')

# add the assist to turnover ratio column
box.statDivision('AST', 'TOV', 'AST/TO')

# add the 3pm per game column
box.statDivision('FG3M', 'GP', '3PM/G')

# add the minutes per game column
box.statDivision('MIN', 'GP', 'MIN/G')

# anything else I should do with this data? or just save to a csv to be outputted to the website?