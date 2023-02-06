import os, sys, pandas as pd

# takes in the data file and the stats columns, initializes csvs, and splits the data into a simplified boxscore
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
    
    # returns the boxscore dataframe
    def getBoxScore(self):
        return self.box

    # returns boxscore with only the columns in colNames
    def setBoxScoreColumns(self, colNames):
        self.box = self.box[colNames]

    # divides the stats in col1 by the stats in col2 and saves the result in newColName
    def statDivision(self, col1, col2, newColName):
        self.box[newColName] = self.box[col1] / self.box[col2]
    
    # multiplies the stats in col1 by the stats in col2 and saves the result in newColName
    def statMultiply(self, col1, col2, newColName):
        self.box[newColName] = self.box[col1] * self.box[col2]

    # sorts the boxscore by the stats in colName and returns the top n players
    def sortBoxScore(self, colName):
        self.box = self.box.sort_values(by=[colName], ascending=False)
    
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