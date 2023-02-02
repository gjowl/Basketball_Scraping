import os, time, requests, random
import pandas as pd

# Functions
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

# main web scraping function
def scraperFunction(per_mode_list, seasons, outputDir, params):
    # loop through the per_mode_list to determine what types of statistics to get 
    for per_mode in per_mode_list:
        modeOutputDir = outputDir + per_mode + '/'
        if params["lastNGames"] != "0":
            modeOutputDir = outputDir + "last" + params["lastNGames"] + "Games/"
        elif params["month"] != "0":
            modeOutputDir = outputDir + "Month" + params["month"] + "/"
        makeOutputDir(modeOutputDir)
        # loop through each season in season list
        for season in seasons:
            # generate a player file and data file for each season
            #player_file = f"{outputDir}{season}_players.csv"
            all_data_file = f"{modeOutputDir}{season}.csv"
            # mandatory wait step to not exceed API rate limit of requests to nba server
            wait()
            # get player data
            nba_df = getDataframeFromWeb(per_mode, season, params)
            # get all of the player names
            #players = nba_df['PLAYER_NAME']
            ## save the player names to a csv file
            #if not os.path.exists(player_file):
            #    players.to_csv(player_file, index=False)
            # save the nba_df to a csv file
            nba_df.to_csv(all_data_file, index=False)
            print(all_data_file + ' saved.')

# function that scrapes the website and returns data in dataframe format
def getDataframeFromWeb(per_mode, season, params):
    # get the necessary options from the config file
    starter_bench        = params["starter_bench"]
    draft_year           = params["draft_year"]
    draft_pick           = params["draft_pick"]
    outcome              = params["outcome"]
    season_type          = params["season_type"]
    period               = params["period"]
    shot_clock_range     = params["shot_clock_range"]
    lastNGames           = params["lastNGames"]
    month                = params["month"]
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
    &GameSegment=&Height=&LastNGames='+lastNGames+'&LeagueID=00&Location=&MeasureType=Base&Month='+month+'&OpponentTeamID=0&Outcome='+outcome+'&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period='+period+'\
    0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season+'&SeasonSegment=&SeasonType='+season_type+'&ShotClockRange=\
    &StarterBench='+starter_bench+'&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
    # get the data from the url
    try:
        response = requests.get(url=player_info_url, headers=headers).json()
    except ValueError:
        print('Error: ' + player_info_url)
        # decide how to handle a server that's misbehaving to this extent
    # Jabe hard-coded column names; I figured out the below to get the column names from the webpage
    column_names = response['resultSets'][0]['headers']
    player_info = response['resultSets'][0]['rowSet']
    nba_df = pd.DataFrame(player_info)
    # set column names of the nba_df to columnNames
    nba_df.columns = column_names
    return nba_df

# define scraping parameters
params = {}
params["starter_bench"] = ''
params["draft_year"] = ''
params["draft_pick"] = ''
params["outcome"] = ''
params["season_type"] = 'Regular+Season'
params["period"] = ''
params["shot_clock_range"] = ''
params["lastNGames"] = '0'
params["month"] = '0'

# get the date
date = time.strftime("%Y-%m-%d")

# define the output directory
outputDir = "/mnt/d/github/Basketball_Scraping/Scripts/NBA_API/"+date+"/"

# define the per_mode_list
per_mode_list = ['PerGame', 'Totals', 'Per100Possessions', 'Per36']

# get the current nba season
currentSeason = time.strftime("%Y")+
currentYear = time.strftime("%Y")
nextYear = str(int(currentYear) + 1) 
seasons = ['2022-23']

# call the scraper function
scraperFunction(per_mode_list, seasons, outputDir, params)

# write in a way to check this every couple of games?
# set this up so that it only runs on certain days of the year: not throughout summer and until the start of the next season, at a certain date it gets playoffs, etc.
# call the scraper function again for the last 10 and last 15 games
per_mode_list = ['PerGame', 'Totals']
params["lastNGames"] = '10'
scraperFunction(per_mode_list, seasons, outputDir, params)
params["lastNGames"] = '15'
scraperFunction(per_mode_list, seasons, outputDir, params)

# call the scraper function again anytime the month changes to get data for the current month
params["lastNGames"] = '0'
params["month"] = '1'
scraperFunction(per_mode_list, seasons, outputDir, params)
