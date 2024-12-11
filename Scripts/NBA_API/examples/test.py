import pandas as pd
import numpy as np
import plotly.graph_objects as go

### Get All teams
from nba_api.stats.static import teams

nba_teams = teams.get_teams()

### Get games of current season
from nba_api.stats.endpoints import leaguegamefinder
games_per_team = []
for team in nba_teams:
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team['id'])
    games = gamefinder.get_data_frames()[0]
    games.GAME_DATE = pd.to_datetime(games.GAME_DATE)
    ### Here i choose games from the current 2023-2024 Season (without pre-season games)
    games_per_team.append(games[(games.SEASON_ID == '22023') & (games.GAME_DATE >= '2023-10-24')])

### Get the Offensive rating, the Defensive rating and other relative stats
from nba_api.stats.endpoints import boxscoreadvancedv3

target_stats = []
for team in games_per_team:
    ### Take number of Win and Losses
    WL = team.WL.value_counts().reset_index()
    W = WL[WL.WL == 'W']['count'].values[0]
    L = WL[WL.WL == 'L']['count'].values[0]
    ### Get classic stats
    target_stats.append({'team_abbreviation':team.TEAM_ABBREVIATION.unique()[0],
                         'team_name':team.TEAM_NAME.unique()[0],
                         'game_date':team.GAME_DATE.to_list(),
                         'W':W,
                         'L':L,
                         'offensive_rating':[], 
                         'defensive_rating':[],
                         'possessions':[] 
                         })
    
    ### Get advanced stats
    for id in team.GAME_ID.to_list():
        stats = boxscoreadvancedv3.BoxScoreAdvancedV3(game_id=id) 
        ### If the team is an away team during the game, you take the stats in the awayTeam key
        if team[team.GAME_ID == id].MATCHUP.values[0][4] == "@":  ### Away Team
            target_stats[-1]['offensive_rating'].append(stats.get_dict()['boxScoreAdvanced']['awayTeam']['statistics']['offensiveRating'])
            target_stats[-1]['defensive_rating'].append(stats.get_dict()['boxScoreAdvanced']['awayTeam']['statistics']['defensiveRating'])
            target_stats[-1]['possessions'].append(stats.get_dict()['boxScoreAdvanced']['awayTeam']['statistics']['possessions'])
        else:
            target_stats[-1]['offensive_rating'].append(stats.get_dict()['boxScoreAdvanced']['homeTeam']['statistics']['offensiveRating'])
            target_stats[-1]['defensive_rating'].append(stats.get_dict()['boxScoreAdvanced']['homeTeam']['statistics']['defensiveRating'])
            target_stats[-1]['possessions'].append(stats.get_dict()['boxScoreAdvanced']['homeTeam']['statistics']['possessions'])

### Compute metrics
data = pd.DataFrame(target_stats)
data['GP'] = data.W + data.L
data['PCT_W'] = (data.W / data.GP)*100
data['PCT_W_rank'] = data.PCT_W.rank(method='min', ascending=False).astype('int64')
data.head()