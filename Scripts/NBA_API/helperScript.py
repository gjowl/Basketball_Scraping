'''
This script will do any final necessary file movement:
 - move config to the output directory
'''

import os, sys, shutil, configparser

# read in the config file
configFile = sys.argv[1]
config = configparser.ConfigParser()
config.read(configFile)
programName = 'helperScript'
dataDir = config[programName]['dataDir']

# move the config file to the data directory
shutil.move(configFile, dataDir)

