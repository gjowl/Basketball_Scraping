import os, sys, time, requests, random, datetime
import pandas as pd

# file to write the output to
file = open(r'D:\github\Basketball_Scraping\Scripts\NBA_API\scriptRunData2.txt', 'a')
file.write(f'Program started at: {datetime.datetime.now()}\n')

## Functions
#def wait():
#    time.sleep(1 + (10 * random.random()))
#
#def makeOutputDir(outputDir):
#    # check if the path to the directory exists
#    if not os.path.isdir(outputDir):
#        print('Creating output directory: ' + outputDir + '.')
#        # the below makes directories for the entire path
#        os.makedirs(outputDir)
#    else:
#        print('Output Directory: ' + outputDir + ' exists.')
#
## main function that scrapes the website and returns data in dataframe format; takes a set of given parameters and
## returns a dataframe of the data
#def getDataframeFromWeb(per_mode, lastNGames, season, params):
#    # get the necessary options from the parameters dictionary
#    starter_bench        = params["starter_bench"]
#    draft_year           = params["draft_year"]
#    draft_pick           = params["draft_pick"]
#    outcome              = params["outcome"]
#    season_type          = params["season_type"]
#    period               = params["period"]
#    shot_clock_range     = params["shot_clock_range"]
#    month                = params["month"]
#    # need this to request through NBA; from this: https://github.com/rd11490/NBA_Tutorials/tree/master/finding_endpoints
#    headers = {
#        'Connection': 'keep-alive',
#        'Accept': 'application/json, text/plain, */*',
#        'x-nba-stats-token': 'true',
#        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
#        'x-nba-stats-origin': 'stats',
#        'Sec-Fetch-Site': 'same-origin',
#        'Sec-Fetch-Mode': 'cors',
#        'Referer': 'https://stats.nba.com/',
#        'Accept-Encoding': 'gzip, deflate, br',
#        'Accept-Language': 'en-US,en;q=0.9',
#    }
#    # url that is used to access the specified data: on nba.com/stats/, go to the webpage of interest, 
#    # right click, inspect element (Q), go to network, search for league, then copy the url
#    player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick='+draft_pick+'&DraftYear='+draft_year+'&GameScope=\
#    &GameSegment=&Height=&LastNGames='+lastNGames+'&LeagueID=00&Location=&MeasureType=Base&Month='+month+'&OpponentTeamID=0&Outcome='+outcome+'&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period='+period+'\
#    0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season+'&SeasonSegment=&SeasonType='+season_type+'&ShotClockRange=\
#    &StarterBench='+starter_bench+'&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
#    # There are a bunch more urls that can be used to get more data; for example, the below url can be used to get the shot locations of each player
#    # need to figure out a way to run through more urls easily instead of just one
#    #shotLocation_url = 'https://stats.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange=By Zone&Division=&DraftPick=&DraftYear=&GameScope=\
#    #&GameSegment=&Height=&LastNGames=0&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N\
#    #&Rank=N&Season=2022-23&SeasonSegment=&SeasonType=Pre Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
#    try:
#        response = requests.get(url=player_info_url, headers=headers).json()
#    # in case there is an error, print the url that caused the error
#    except ValueError:
#        print('Error: ' + player_info_url)
#    # get column names and data for each player from the response
#    column_names, data = response['resultSets'][0]['headers'], response['resultSets'][0]['rowSet']
#    # convert the player_info to a dataframe
#    nba_df = pd.DataFrame(data)
#    # set column names of the nba_df to columnNames
#    nba_df.columns = column_names
#    return nba_df
#
## set the per_mode and season from the config file
#per_mode = ["PerGame", "Per36", "Totals", "Per100Possessions"]
#season = "2022-23"
#lastNGames = ["15"]
#
## make the output directory
#date = time.strftime("%Y-%m-%d")
## define the output directory for windows
#outputDir = os.path.join(os.getcwd(), 'output', date)
#makeOutputDir(outputDir)
#
## setup the parameters for the getDataframeFromWeb function
#parameters = {
#    "starter_bench": "",
#    "draft_year": "2022",
#    "draft_pick": "",
#    "outcome": "",
#    "season_type": "Regular+Season",
#    "period": "",
#    "shot_clock_range": "",
#    "month": "0"
#}
#
## retrieve data from nba.com for each per_mode
#for mode in per_mode:
#    # loop through the lastNGames
#    # check if the output directory exists
#    output = outputDir + '/' + mode
#    makeOutputDir(output) 
#    for lastN in lastNGames:
#        nba_df = getDataframeFromWeb(mode, lastN, season, parameters)
#        # define the file name for the data
#        filename =  output + '/' + lastN + 'games.csv'
#        # save the nba_df to a csv file
#        nba_df.to_csv(filename, index=False)
#
#file.write(f'Files saved to: {outputDir}\n')
#file.write(f'Program ended at: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')