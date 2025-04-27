import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import plot_quadrant_scatter, get_player_data, get_player_ranks, create_player_rank_bar_graph, make_year_scatterplot, create_year_data_dict

# SET PAGE CONFIG
st.set_page_config(page_title='Player Rankings',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('🔍 Player Rankings')

# VARIABLES 
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
#datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
#contains = 'all_game' # file you want to read
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD'
advancedDir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
contains = '2023-24_boxscore' # file you want to read
colors = '/mnt/d/github/Basketball_Scraping/site/team_colors_hex.csv'
options = '/mnt/d/github/Basketball_Scraping/site/options.csv'

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

## VARIABLES FOR THE STATS TO GET
name_and_year = ['PLAYER_NAME', 'YEAR']
cols_to_keep = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MPG'] # keep the player name, team abbreviation, and GP
shooting = ['FG%', 'FGA_PG', 'FGM_PG', '2P%', '2PA_PG', '2PM_PG', '3P%', '3PA_PG', '3PM_PG', 'FT%', 'FTA_PG', 'FTM_PG'] # make into quadrant plots
traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV_PG', 'PF_PG']
advanced = ['AST_TO', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%']
rank_cols = [traditional, shooting, advanced]
check_gp = False
gp, plot_number = 0, 0

# FUNCTIONS
def get_ranks(_data, _stat_list, _season=True):
    player_ranks = pd.DataFrame()
    for stat in _stat_list:
        if player_ranks.empty:
            if _season == False:
                player_ranks = _data[['PLAYER_NAME', 'TEAM_ABBREVIATION']].copy()
            else: 
                # add the player name and year to the dataframe
                player_ranks = _data[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'SEASON', 'YEAR']].copy()
        # calculate the percentile for each stat
        _data[f'{stat}_Percentile'] = _data[stat].rank(pct=True)
        # create a ranked list column based on the percentile of the stat
        _data[f'{stat}_Rank'] = _data[stat].rank(ascending=False)
        player_ranks = pd.concat([player_ranks, _data[[f'{stat}_Percentile', f'{stat}_Rank']]], axis=1)
    return player_ranks

def get_season_player_rankings(_year_data_dict, _advanced_data_dict, _rank_cols, _check_gp, _gp):
    all_ranks = []
    for ranks in _rank_cols:
        # get the player rankings for the season
        tmp_df = pd.DataFrame()
        for key in _year_data_dict.keys():
            season_df = _year_data_dict[key]
            # remove data for players with less than games played
            if 'TS%' in ranks:
                season_df = _advanced_data_dict[key]
            if _check_gp:
                season_df = season_df[season_df['GP'] >= _gp]
                # get the player rankings for the season
                player_ranks = get_ranks(season_df, ranks)
                tmp_df = pd.concat([tmp_df, player_ranks], ignore_index=True)
            else:
                player_ranks = get_ranks(season_df, ranks)
                tmp_df = pd.concat([tmp_df, player_ranks], ignore_index=True)
        all_ranks.append(tmp_df)
    return all_ranks

def get_all_time_player_rankings(_year_data_dict, _advanced_data_dict, _rank_cols, _check_gp, _gp):
    all_ranks = []
    for ranks in _rank_cols:
        # get the player rankings for the season
        tmp_df = pd.DataFrame()
        for key in _year_data_dict.keys():
            season_df = _year_data_dict[key]
            if 'TS%' in ranks:
                season_df = _advanced_data_dict[key]
            # remove data for players with less than games played
            if _check_gp:
                season_df = season_df[season_df['GP'] >= _gp]
            tmp_df = pd.concat([tmp_df, season_df], ignore_index=True)
        # get the mean for each stat in the rank list
        avg_df = tmp_df.groupby('PLAYER_NAME')[ranks].mean().reset_index()
        # append the first team abbreviation to the dataframe
        avg_df['TEAM_ABBREVIATION'] = tmp_df.groupby('PLAYER_NAME')['TEAM_ABBREVIATION'].first().values
        tmp_ranks = get_ranks(avg_df, ranks, _season=False)
        #st.dataframe(tmp_ranks, use_container_width=True, hide_index=True)
        all_ranks.append(tmp_ranks)
    return all_ranks

def transform_ranks_for_plotting(_df):
    # separate by _ into index and stat
    ranks, percentiles = _df.columns[_df.columns.str.contains('_Rank')].tolist(), _df.columns[_df.columns.str.contains('_Percentile')].tolist() 
    # separate ranks by _
    ranks, percentiles = [rank.split('_Rank')[0] for rank in ranks], [percentile.split('_Percentile')[0] for percentile in percentiles]
    player_ranks = pd.DataFrame()
    for stat in ranks:
        player_ranks[stat] = [_df[f'{stat}_Percentile'].values[0], _df[f'{stat}_Rank'].values[0]]
    player_ranks = player_ranks.T
    player_ranks.columns = ['Percentile', 'Rank']
    return player_ranks
# MAIN
## PAGE SETUP BELOW
## SELECT A PLAYER FROM THE DROPDOWN
## TABS SEPARATED STATS AND GRAPHS
## BUTTON TO SHOW PLAYER DATA

# LOAD IN THE DATA
year_data_dict, advanced_data_dict = create_year_data_dict(datadir), create_year_data_dict(advancedDir)
## get all the unique player names from the year_data_dict
player_names = pd.Series()
for key in year_data_dict.keys():
    player_names = pd.concat([player_names, year_data_dict[key]['PLAYER_NAME']])
player_names = player_names.unique()

# TOGGLE FOR GP THRESHOLD
if st.toggle('**GP Threshold**'):
    # add in a slider for the number of games played
    gp = st.slider('Number of games played', 0, 82, 65)
    check_gp = True

# GET RANKINGS FOR ALL PLAYERS
all_ranks = get_season_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp)

## TABS START HERE
tabs = st.tabs(['Player Search', 'Rank Finder'])

# TAB 1: PLAYER SEARCH
with tabs[0]:
    ## SELECT A PLAYER FROM THE DROPDOWN
    player = st.selectbox('*Select a player to load data and graphs*', player_names, index=0, placeholder='Player Name...')
    #player = st.selectbox('*Select a player to load data and graphs*', player_names, index=None, placeholder='Player Name...')
    #if player is None:
    #    st.warning('My Personal Recs: Mo Williams, Taj Gibson, Danny Green')
    #    st.stop()
    ## get the data for the player from all years they played in the league
    player_dfs = []
    for df in all_ranks:
        player_df = df[df['PLAYER_NAME'] == player].reset_index(drop=True)
        player_dfs.append(player_df)
    titles = ['Traditional', 'Shooting', 'Advanced']
    # differentiate here: seasonal or career
    if st.toggle('**Compare by season**', key='compare_season', value=True):
        season = st.selectbox('Select the season of interest', player_dfs[0]['YEAR'].unique(), key=f'season_{plot_number}')
        for ranks,df,title in zip(rank_cols, player_dfs, titles):
            player_df = df[df['PLAYER_NAME'] == player].reset_index(drop=True)
            season_df = player_df[player_df['YEAR'] == season].reset_index(drop=True)
            player_gp = player_df['GP'].max()
            if gp > player_gp:
                st.warning(f'Player has only played {player_gp} games this season. Please select a lower number of games played.')
                st.stop()
            st.dataframe(season_df, use_container_width=True, hide_index=True)
            player_ranks = transform_ranks_for_plotting(season_df) 
            st.dataframe(player_ranks, use_container_width=True, hide_index=True)
            create_player_rank_bar_graph(season_df, player_ranks, player, title, team_colors, plot_number) 
            plot_number += 1
    else:
        all_time_ranks = get_all_time_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp)
        for df,title in zip(all_time_ranks,titles):
            player_df = df[df['PLAYER_NAME'] == player].reset_index(drop=True)
            player_ranks = transform_ranks_for_plotting(player_df) 
            create_player_rank_bar_graph(player_df, player_ranks, player, title, team_colors, plot_number) 
            plot_number += 1
        st.write('Currently working on implementing this feature!')
# TAB 2: STAT SEARCH
## SELECT A STAT TO PLOT
output_df = pd.DataFrame()
with tabs[1]:
    #st.write('**PLAYER** is **#RANK** in **STAT**, averaging **VAL** for the **SEASON**')
    all_rank_cols = pd.concat(all_ranks, ignore_index=True)
    df = all_ranks[0]
    stat_list = all_rank_cols.columns[all_rank_cols.columns.str.contains('_Rank')].tolist()
    # remove rank from the stat list
    stat_list = [stat.split('_Rank')[0] for stat in stat_list]
    stat = st.selectbox('Select a stat', stat_list, index=None, placeholder='Stat Name...')
    season = st.selectbox('Select the season', df['YEAR'].unique(), key=f'season_{plot_number}')
    season_df = df[df['YEAR'] == season].reset_index(drop=True)
    rank, percentile = f'{stat}_Rank', f'{stat}_Percentile'
    # get a list of the number of ranks in the league
    rank_list = sorted(season_df[rank].unique(), reverse=False)
    # convert the rank list to a list of int
    rank_list = [int(rank) for rank in rank_list if str(rank) != 'nan']
    rank_num = st.selectbox('Select a rank', rank_list, index=None, placeholder='Rank...')
    # get the x ranked player
    player = season_df[season_df[rank] == rank_num]['PLAYER_NAME'].values[0]
    # get the actual stat value for the player
    data_df = year_data_dict[season]
    stat_value = data_df[data_df['PLAYER_NAME'] == player][stat].values[0]
    # add the values to the df 
    tmp_df = pd.DataFrame({'PLAYER_NAME': [player], 'RANK': [rank_num], 'STAT': [stat], 'VALUE': [stat_value], 'SEASON': [season]})
    #output_df = pd.concat([output_df, tmp_df], ignore_index=True)
    st.write(f'In the **{season}** season, **{player}** averaged **{round(stat_value,2)}**  **{stat}** good for **#{rank_num}** in the league.')
    # TODO: if possible, make this like queereable where it shows up to the last x searches (like a search history)

if st.button(f'Show All {player} Data'):
    # show all the data with no scroll bar
    player_df = get_player_data(year_data_dict, player)
    st.dataframe(player_df, use_container_width=True, hide_index=True)
    st.button('Hide Data', key=f'hide_{player}_data')
# an interesting alternate idea (or maybe concurrent) is to basically make the website a scrolling timeline of the player: Kind of like the spotify wrapped, but a timeline of the player with 
# their most important stats and their overall impact on the game? Would some sort of impact on the game metric be interesting? How would I define that just using stats?
# I think I have to start with the most impactful players: Steph is an outlier in 3pt shooting all time. But whenever it started (so he has a large difference in 3PAs to how quickly it gets closer)
# could look at something like that? As if the player is a trendsetter if they are an outlier in a stat and the rest of the league (or at least a certain number of players follows suit?)
