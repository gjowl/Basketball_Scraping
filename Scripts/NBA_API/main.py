import requests
import pandas as pd
import time
import os
import random
"""
The below code is adapted from from the following source:
LearnWithJabe: https://www.youtube.com/watch?v=IELK56jIsEo&ab_channel=LearnWithJabe
"""
# wait for a random amount of time between 1 and 10 seconds (to avoid being blocked as a bot)
def wait():
    time.sleep(1 + (10 * random.random()))
per_mode_list = ['Totals', 'PerGame', 'Per36', 'Per100Possessions', 'Per100Plays']
#season_id_list = ['2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
season_type = 'Regular+Season'
season_id_list = ['2019-20', '2020-21']
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
# set up the output directory to the current directory
output_dir = os.getcwd()+'/'
print(output_dir)
for per_mode in per_mode_list:
    for season_id in season_id_list:
        player_file = f"{output_dir}{season_id}_players.csv"
        column_names_file = f"{output_dir}{per_mode}_{season_id}_columns.csv"
        all_data_file = f"{output_dir}{per_mode}_{season_id}.csv"
        wait()
        print(all_data_file)
        player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=DraftYear=&GameScope=\
        &GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period=\
        0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season_id+'&SeasonSegment=&SeasonType='+season_type+'&ShotClockRange=\
        &StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
        # get the data from the url
        response = requests.get(url=player_info_url, headers=headers).json()
        # Jabe hard-coded column names; I figured out the below to get the column names from the webpage
        column_names = response['resultSets'][0]['headers']
        player_info = response['resultSets'][0]['rowSet']
        nba_df = pd.DataFrame(player_info)
        # set column names of the nba_df to columnNames
        nba_df.columns = column_names
        # get all of the player names
        players = nba_df['PLAYER_NAME']
        # save the player names to a csv file
        if not os.path.exists(player_file):
            players.to_csv(player_file, index=False)
        # save the column names to a csv file
        #column_names.to_csv(column_names_file, index=False)
        # save the nba_df to a csv file
        nba_df.to_csv(all_data_file, index=False)