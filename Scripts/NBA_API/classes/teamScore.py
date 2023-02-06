import os, sys, pandas as pd

# initializes a class object to hold boxscore data for a specific team, a sub-class of boxScore
class teamScore:
    def __init__(self, box):
        self.team = None
        self.box = box

    # sets the team for the teamScore object 
    def setTeam(self, team):
        self.team = team
        self.box = self.box[self.box['TEAM_ABBREVIATION'] == self.team]

    def getBoxScore(self):
        return self.box 

    # TODO: I recently had an idea for a graph that would show a team's performance over the course of a season.
    # it can be used to compare teams and see how they perform over the course of a season and compare to other teams
    # all time (thinking of some sort of circle graph with different stats, normalized per season). Add those functions below
    # I wonder if I can just take percentages of stat per team per year (3pt attempts per team / 3pt attempts per league) and
    # then plot those and see what it gets me?
