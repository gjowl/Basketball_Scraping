import os, sys, pandas as pd
from classes.teamBoxScore import teamBoxScore
from classes.playerBoxScore import playerBoxScore 

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

    # calculate usage rate
    # https://www.reddit.com/r/nba/comments/5p7h1g/lets_talk_about_usage_rate_and_how_to_use_it/
    # 100 * ((FGA + 0.44 * FTA + TOV) * (Tm MP / 5)) / (MP * (Tm FGA + 0.44 * Tm FTA + Tm TOV))
    def calcUsage(self):
        df = self.box
        # get the team data for calculating usage rate
        cols = ['MIN', 'FGA', 'FTA', 'TOV']
        df = self.getTeamData(df, cols)
        # put the minutes, field goals attempted, free throws attempted, turnovers, and team stats into variables
        minutes, fga, fta, asts, tov = df['MIN'], df['FGA'], df['FTA'], df['AST'], df['TOV']
        teamFga, teamFta, teamTov, teamMin = df['TEAM_FGA'], df['TEAM_FTA'], df['TEAM_TOV'], df['TEAM_MIN']
        # calculate usage rate
        df['USG%'] = 100 * ((fga + 0.44 * fta + tov) * (teamMin/5)) / (minutes * (teamFga + 0.44 * teamFta + teamTov))
        # if minutes < 10, set usage rate to 0
        df.loc[df['MIN'] < 10, 'USG%'] = 0
        self.box = df

    # helper function for calculating player usage rate; can also be used to get other team stats for calculating percentages 
    # (i.e. field goal attempt % per player = FGA / TEAM_FGA, etc.)
    def getTeamData(self, df, cols):
        outputDf = pd.DataFrame()
        # loop through unique TEAM_ABBREVIATION
        for team in df['TEAM_ABBREVIATION'].unique():
            teamDf = df[df['TEAM_ABBREVIATION'] == team].copy()
            for col in cols:
                # get the data for the team
                teamDf['TEAM_' + str(col)] = teamDf.loc[teamDf['TEAM_ABBREVIATION' == team, col]].sum()
            outputDf = pd.concat([outputDf, teamDf])
        return outputDf

    # returns the boxscore dataframe
    def getBoxScore(self):
        return self.box

    # return the data for a team into a teamData object
    def getTeamBoxScore(self, team):
        score = teamBoxScore(self.box)
        score.setTeam(team)
        return score

    # return the data for a player into a playerData object
    def getPlayerBoxScore(self, player):
        score = playerBoxScore(self.box)
        score.setPlayer(player)
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