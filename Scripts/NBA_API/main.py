import os
import sys
from functions import *

"""
The below code is adapted from from the following source:
LearnWithJabe: https://www.youtube.com/watch?v=IELK56jIsEo&ab_channel=LearnWithJabe

It gets player data from NBA.com and saves it to a csv file.

By generating a config file with the options shown below, you can run the code
and get player data for a variety of seasons (Regular, Playoffs, Preseason), draft picks,
outcomes (Wins, Losses), shot clock ranges (24-22, 22-18, 18-15, 15-7, 7-4, 4-0), and
periods (1, 2, 3, 4, 5, 6, 7, 8; 5, 6, 7, and 8 are overtimes).

In the future, would be nice to make this code more specific: get certain teams, get certain players, etc.
But for now, it gets the data for all players that played in the season, and other scripts can be used to filter the data.

ADD SCRIPTS BELOW ONCE THEY ARE COMPLETE
"""

# Use the function to get the configFile
configFile = sys.argv[1]

# Use the utilityFunctions function to get the name of this program
programName = getFilename(__file__)

# Read in configuration file:
globalConfig = read_config(configFile)
config = globalConfig[programName]

# Config file options:
outputDir            = config["outputDir"]
season_list          = config["season_list"]
requirementsFile     = config["requirementsFile"]

# returns seasons list in format of '2012-13', '2013-14', etc.
seasons = getSeasonList(season_list)

if __name__ == '__main__':
    # make the output directory that these will all output to
    makeOutputDir(outputDir)

    # install requirements
    installRequiredPackages(requirementsFile)
    
    # loop through each mode of data
    per_mode_list = ['Totals', 'PerGame', 'Per36', 'Per100Possessions', 'Per100Plays']
    scraperFunction(per_mode_list, seasons, config)
    
