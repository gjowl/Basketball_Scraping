import requests
import pandas as pd
"""
The below code is adapted from from the following source:
LearnWithJabe: https://www.youtube.com/watch?v=IELK56jIsEo&ab_channel=LearnWithJabe
"""

# TODO: this may have to be hardcoded? I don't know how else to get a list of these from NBA.com
per_mode = 'Totals'
# TODO: make the season list dynamic; Jabe hard-coded the season list
season_id = '2018-19'
player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season_id+'&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
# need this to request through NBA; from this: https://github.com/rd11490/NBA_Tutorials/tree/master/finding_endpoints
headers  = {
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
response = requests.get(url=player_info_url, headers=headers).json()
# Jabe hard-coded column names; I figured out the below to get the column names from the webpage
columnNames = response['resultSets'][0]['headers']
player_info = response['resultSets'][0]['rowSet']
nba_df = pd.DataFrame(player_info)

# set column names of the nba_df to columnNames
nba_df.columns = columnNames
print(nba_df.sample(10))

#nba_df.to_csv('nba_df.csv', index=False)