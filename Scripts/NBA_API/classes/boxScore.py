import os, sys, pandas as pd
from classes.teamScore import teamScore

# initializes an class object to hold the data file. Contains simple functions for handling data
class boxScore:
    # constructor
    def __init__(self):
        # instance variable
        self.box = None
    
    def setBoxScore(self, dataFile):
        # read in the input data from the command line
        data = pd.read_csv(dataFile)
        # keep only the stats columns
        self.box = data
    
    # returns boxscore with only the columns in colNames
    def extractBoxScoreColumns(self, colNames):
        return self.box[colNames]

    # divides the stats in col1 by the stats in col2 and saves the result in newColName to 3 significant figures
    def statDivision(self, col1, col2, newColName):
        self.box[newColName] = (self.box[col1] / self.box[col2]).round(2) 

    # multiplies the stats in col1 by the stats in col2 and saves the result in newColName
    def statMultiply(self, col1, col2, newColName):
        self.box[newColName] = self.box[col1] * self.box[col2].round(2)

    # sorts the boxscore by the stats in colName and returns the top n players
    def sortBoxScore(self, colName):
        self.box = self.box.sort_values(by=[colName], ascending=False)

    # imposes a limit for a stat in the boxscore (i.e. only keep players with more than 10 points per game)
    def imposeLimit(self, colName, limit):
        self.box = self.box[self.box[colName] > limit]

    # returns the boxscore dataframe
    def getBoxScore(self):
        return self.box

    def getTeamScore(self, team):
        score = teamScore(self.box)
        score.setTeam(team)
        return score

    # returns the top n players in the boxscore
    def topN(self, n):
        return self.box.head(n)

    # returns the bottom n players in the boxscore
    def bottomN(self, n):
        return self.box.tail(n)
    
    # returns the top n players in the boxscore sorted by colName
    def topNBy(self, n, colName):
        return self.box.sort_values(by=[colName], ascending=False).head(n)
    
    # returns the bottom n players in the boxscore sorted by colName
    def bottomNBy(self, n, colName):
        return self.box.sort_values(by=[colName], ascending=True).head(n)