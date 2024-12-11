import os, configparser, time, random, requests
import pandas as pd
"""
This file includes functions that are used in the main.py script.
"""

# wait for a random amount of time between 1 and 10 seconds (to avoid being blocked as a bot)
def wait():
    time.sleep(1 + (10 * random.random()))

def makeOutputDir(outputDir):
    # check if the path to the directory exists
    if not os.path.isdir(outputDir):
        print('Creating output directory: ' + outputDir + '.')
        # the below makes directories for the entire path
        os.makedirs(outputDir)
    else:
        print('Output Directory: ' + outputDir + ' exists.')

# get filename separate from type and directory
def getFilename(file):
    programPath = os.path.realpath(file)
    programDir, programFile = os.path.split(programPath)
    filename, programExt = os.path.splitext(programFile)
    return filename

# Helper file for reading the config file of interest for running the program
def read_config(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
    return config

#install required packages for the below programs; these are found in requirements.txt
#if you decide to add more packages to these programs, execute the below and it will update the requirements file:
#   -pip freeze > requirements.txt
#tips for requirements files:
#  https://pip.pypa.io/en/latest/reference/requirements-file-format/#requirements-file-format
#  gets rid of requirement output: https://github.com/pypa/pip/issues/5900?msclkid=474dd7c0c72911ec8bf671f1ae3975f0
def installRequiredPackages(requirementsFile):
    execInstallRequirements = "pip install -r " + requirementsFile + " | { grep -v 'already satisfied' || :; }" 
    os.system(execInstallRequirements)

# main web scraping function
def scraperFunction(per_mode_list, seasons, config):
    # get the necessary options from the config file
    outputDir            = config["outputDir"]
    # loop through the per_mode_list to determine what types of statistics to get 
    for per_mode in per_mode_list:
        modeOutputDir = outputDir + per_mode + '/'
        makeOutputDir(modeOutputDir)
        # loop through each season in season list
        for season in seasons:
            # generate a player file and data file for each season
            #player_file = f"{outputDir}{season}_players.csv"
            all_data_file = f"{modeOutputDir}{season}.csv"
            # mandatory wait step to not exceed API rate limit of requests to nba server
            wait()
            # get player data
            nba_df = getDataframeFromWeb(per_mode, season, config)
            # get all of the player names
            #players = nba_df['PLAYER_NAME']
            ## save the player names to a csv file
            #if not os.path.exists(player_file):
            #    players.to_csv(player_file, index=False)
            # save the nba_df to a csv file
            nba_df.to_csv(all_data_file, index=False)
            print(all_data_file + ' saved.')

# create a list of seasons to get data for from first_season to last_season
def getSeasonList(season_list):
    first_season = int(season_list.split('-')[0])
    last_season = int(season_list.split('-')[1])
    season_list = []
    for i in range(first_season, last_season):
        seasonStart = str(i)
        seasonEnd = str(i+1)
        # check if seasonStart and seasonEnd are in same century
        if seasonStart[0] == seasonEnd[0]:
            season_list.append(seasonStart + '-' + seasonEnd[2] + seasonEnd[3])
        else:
            season_list.append(seasonStart + '-' + seasonEnd)
    return season_list

# function that scrapes the website and returns data in dataframe format
def getDataframeFromWeb(per_mode, season, config):
    # get the necessary options from the config file
    starter_bench        = config["starter_bench"]
    draft_year           = config["draft_year"]
    draft_pick           = config["draft_pick"]
    outcome              = config["outcome"]
    shot_clock_range     = config["shot_clock_range"]
    season_type          = config["season_type"]
    period               = config["period"]
    
    # need this to request through NBA; from this: https://github.com/rd11490/NBA_Tutorials/tree/master/finding_endpoints
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    # url that is used to access the specified data: on nba.com/stats/, go to the webpage of interest, 
    # right click, inspect element (Q), go to network, search for league, then copy the url
    player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick='+draft_pick+'DraftYear='+draft_year+'&GameScope=\
    &GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome='+outcome+'&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period='+period+'\
    0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season+'&SeasonSegment=&SeasonType='+season_type+'&ShotClockRange=\
    &StarterBench='+starter_bench+'&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
    # get the data from the url
    response = requests.get(url=player_info_url, headers=headers).json()
    # Jabe hard-coded column names; I figured out the below to get the column names from the webpage
    column_names = response['resultSets'][0]['headers']
    player_info = response['resultSets'][0]['rowSet']
    nba_df = pd.DataFrame(player_info)
    # set column names of the nba_df to columnNames
    nba_df.columns = column_names
    return nba_df