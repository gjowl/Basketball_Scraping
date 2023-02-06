import os, sys, time, requests, random, configparser
import pandas as pd

# get filename separate from type and directory
def getFilename(file):
    programPath = os.path.realpath(file)
    programDir, programFile = os.path.split(programPath)
    filename, programExt = os.path.splitext(programFile)
    return filename

# get the current working directory
cwd = os.getcwd()

# Use the function to get the configFile
configFile = sys.argv[1]

# Use the utilityFunctions function to get the name of this program
programName = getFilename(__file__)

# get the date
date = time.strftime("%Y-%m-%d")

# get the current nba season
""" TODO:
 - check if the date is before the playoffs
 - have a way to automate getting the date and the current season
 - think of an easy way to write this so that I can quickly change something in another file and have it update here
 - write in a way to check this every couple of games?
 - set this up so that it only runs on certain days of the year: not throughout summer and until the start of the next season, at a certain date it gets playoffs, etc.
 - eventually: set up so that this also runs an analysis and updates on my website (Paul George has made at least 4 3s in the last 5 games, etc.)
"""
if __name__ == '__main__':
    # get the current nba season
    # check and make sure the requirements are met
    # install the requirements
    # run the nbaStatsPullRequest.py script
    pullRequest = f'python3 nbaStatsPullRequest.py {configFile} {programName} {date}' 
    os.system(pullRequest)

    # TODO: create an analysis script that runs after the nbaStatsPullRequest.py script
    outputDir = cwd + '/' + date
    # loop through the files in the output directory
    for file in os.listdir(outputDir):
        analyzeFile = f'python3 nbaStatsAnalysis.py {file}'
        os.system(analyzeFile) # date in this case is the output directory

    # create a pull request to get shooting data from different spots and an analysis method for that too
    # create a way to pull the data from the last day of games from nba.com
