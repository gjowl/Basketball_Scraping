import os, sys, datetime, time, random
'''
This file is the main file that runs the other scripts in the NBA_API folder. It is the file that you should run to get the data from the NBA_API.
'''

# define the variables (hardcoded)
scriptDir = r'D:/github/Basketball_Scraping/Scripts/NBA_API'
outputDir = r'H:/NBA_API_DATA'

# make the paths for the scripts
scraper = os.path.join(scriptDir, 'scraper.py')
setupBoxscore = os.path.join(scriptDir, 'setupBoxscore.py')
graphData = os.path.join(scriptDir, 'graphData.py')
# run the exampleTask.py script
os.system(f'python3 {scraper}')
# run the setupBoxscore.py script
datafile = f'{outputDir}/finalBoxscore.csv'
os.system(f'python3 {setupBoxscore} {datafile} {outputDir}')
# run the graphData.py script
os.system(f'python3 {graphData} {datafile} {outputDir}')