import os, sys, pandas as pd

# initializes a class object to hold boxscore data for a specific team, a sub-class of boxScore
class teamScore:
    def __init__(self, box):
        self.player = None
        self.box = box

    # sets the player for the playerScore object 
    def setPlayer(self, player):
        self.player = player
        self.box = self.box[self.box['PLAYER_NAME'] == self.player]

    def getBoxScore(self):
        return self.box 
