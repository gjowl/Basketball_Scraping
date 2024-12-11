import os, sys, configparser, pandas as pd, numpy as np, time, matplotlib.pyplot as plt
from classes.boxScore import boxScore

'''
This script will take boxscore data and calculate some stats that might be interesting for fantasy basketball.

It will also output some graphs for each of these stats
'''

# read in the config file
configFile = sys.argv[1]
config = configparser.ConfigParser()
config.read(configFile)
programName = 'fantasyCornerStats'
dataDir = config[programName]['dataDir']
file1 = config[programName]['file1']
file2 = config[programName]['file2']
outputDir = config[programName]['graphDir']

# Functions



# read in the data

# initialize the boxscore object
box1 = boxScore()
box2 = boxScore()

# set the boxscore
box1.setBoxScore(file1)
box2.setBoxScore(file2)

# subtract the boxscores
box3 = box1 - box2

# create bar graphs of the top 5 differences (+ and -) for each of the following stats