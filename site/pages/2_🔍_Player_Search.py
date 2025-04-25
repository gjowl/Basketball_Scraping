import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import plot_quadrant_scatter, get_player_data, get_player_ranks, create_player_rank_bar_graph, make_year_scatterplot, create_year_data_dict

# SET PAGE CONFIG
st.set_page_config(page_title='Player Search',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Player Search')

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
percent = ['FG%', '2P%', '3P%']
shots_types = [['FG%', 'FGA_PG', 'FGM_PG'], ['2P%', '2PA_PG', '2PM_PG'], ['3P%', '3PA_PG', '3PM_PG'], ['FT%', 'FTA_PG', 'FTM_PG']] # make into quadrant plots
shot_pairs = [['FGA_PG', 'FGM_PG'], ['2PA_PG', '2PM_PG'], ['3PA_PG', '3PM_PG'], ['FTA_PG', 'FTM_PG']]

traditional_groups = [['MPG', 'PPG', 'APG'], ['RPG', 'SPG', 'BPG'], ['AST_TO', 'TOV_PG', 'PF_PG']] # unsure yet
quadrant_pairs = [['PPG', 'APG'], ['APG', 'TOV_PG'], ['RPG', 'BPG'], ['OREB_PG', 'DREB_PG'], ['SPG', 'PF_PG']] # make into quadrant plots

shooting = ['FG%', 'FGA_PG', 'FGM_PG', '2P%', '2PA_PG', '2PM_PG', '3P%', '3PA_PG', '3PM_PG', 'FT%', 'FTA_PG', 'FTM_PG'] # make into quadrant plots
traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV_PG', 'PF_PG']
advanced = ['AST_TO', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%']
rank_cols = [traditional, shooting, advanced]
check_gp = False
gp = 0

# FUNCTIONS
def seasonal_ranks(_season_df, _player, _cols, _gp, _n=0):
    if _gp > 0:
        # filter the dataframe to only include players with more than 10 games played
        _season_df = _season_df[_season_df['GP'] > _gp]
    # get the player rankings for the player in the season
    player_ranks = get_player_ranks(_season_df, _player, _cols)
    create_player_rank_bar_graph(_season_df, player_ranks, player, team_colors, _n)

# MAIN
## PAGE SETUP BELOW
## SELECT A PLAYER FROM THE DROPDOWN
## TABS SEPARATED STATS AND GRAPHS
## BUTTON TO SHOW PLAYER DATA

## TODO: clean this code up
## TODO: add a blurb about the page and what it does
# TODO: get a average for all years for each stat and plot as another line; gives context to the player being an outlier or not
# TODO: fix the line color and just always show lines

# LOAD IN THE DATA
year_data_dict = create_year_data_dict(datadir)
advanced_data_dict = create_year_data_dict(advancedDir)
## get all the unique player names from the year_data_dict
player_names = pd.Series()
for key in year_data_dict.keys():
    player_names = pd.concat([player_names, year_data_dict[key]['PLAYER_NAME']])
player_names = player_names.unique()

## SELECT A PLAYER FROM THE DROPDOWN
player = st.selectbox('*Select a player to load data and graphs*', player_names, index=None, placeholder='Player Name...')
if player is None:
    st.warning('My Personal Recs: Mo Williams, Taj Gibson, Danny Green')
    st.stop()
# TODO: add a list of recommended players to the dropdown

## get the data for the player from all years they played in the league
player_df = get_player_data(year_data_dict, player)

if st.toggle('**GP Threshold**'):
    # add in a slider for the number of games played
    gp = st.slider('Number of games played', 0, 82, 65)
    check_gp = True

## TABS 
tabs = st.tabs(['**Rankings**', '**Shooting**', '**Advanced**']) # add in advanced as well

plot_number = 0
for tab in tabs:
    with tab:
        season = st.selectbox('Select the season of interest', player_df['YEAR'].unique(), key=f'season_{plot_number}')
        for cols in rank_cols:
            # check if it's the advanced tab
            if 'TS%' in cols:
                season_df = advanced_data_dict[season]
                seasonal_ranks(season_df, player, cols, gp, plot_number)
            else:
                season_df = year_data_dict[season]
                seasonal_ranks(season_df, player, cols, gp, plot_number)
            plot_number += 1
    # TODO: add in a blurb here about the rankings and what they mean
    # probably something about how they are ranked top x in the league for top 3 stats
    # could make it pseudo dynamic. For example: Lebron is probably gonna have years where he is top 3 in PPG, APG, RPG. And thne maybe top 10-50 in others that could also be mentioned 
#with tab2:
#    st.header(f'{player} Shooting Stats Trajectory by Year')
#    # TODO: show the boxscore data for the player
#    if st.button('Show Shooting Data'):
#        st.write('Below are the shooting stats for the player')
#        st.dataframe(player_df, use_container_width=True, hide_index=True)
#        st.button('Hide Shooting Data')
#    # add a toggle to add a line to the plot for the average of the stat
#    for shots in shots_types:
#        figs = []
#        for shot in shots:
#            fig = make_year_scatterplot(player_df, shot, team_colors)
#            figs.append(fig)
#            n+=1
#        cols = st.columns(3)
#        for fig, col in zip(figs, cols):
#            with col:
#                st.plotly_chart(fig, key=n, use_container_width=True)
#                n+=1
#with tab3:
#    st.header('Traditional Stats Trajectory by Year')
#    # TODO: show the boxscore data for the player
#    if st.button('Show Non-Shooting Data', key='nonshooting'):
#        st.write('Below are the non-shooting stats for the player')
#        st.dataframe(player_df, use_container_width=True, hide_index=True)
#        st.button('Hide Non-Shooting Data', key='hide_nonshooting')
#    for group in traditional_groups:
#        figs = []
#        for stat in group:
#            fig = make_year_scatterplot(player_df, stat, team_colors)
#            figs.append(fig)
#            n+=1
#        cols = st.columns(3)
#        for fig, col in zip(figs, cols):
#            with col:
#                st.plotly_chart(fig, key=n, use_container_width=True)
#                n+=1
#        # TODO: show the legend on the right side of the plots
#with tab4:
#    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
#    advanced_data_dict = create_year_data_dict(datadir)
#    ## get the data for the player from all years they played in the league
#    player_df = get_player_data(advanced_data_dict, player)
#
#    # change the YEAR column to be SEASON, keep the split by _
#    player_df['SEASON'] = player_df['YEAR'].str.split('-').str[0]
#
#    # read in the advanced stats data
#    stats = ['W%', 'TS%', 'USG%', 'AST%', 'OREB%', 'DREB%', 'REB%', 'POSS_PG', 'EFG%']
#    for stat in stats:
#        fig = make_year_scatterplot(player_df, stat, team_colors)
#        st.plotly_chart(fig, use_container_width=True)
#    ranks = ['OFF_RATING_RANK', 'DEF_RATING_RANK', 'AST%_RANK', 'AST_TO_RATIO_RANK', 'AST_PCT_RANK', 'STL_PCT_RANK', 'BLK_PCT_RANK', 'OREB%_RANK', 'DREB%_RANK', 'REB%_RANK', 'TS%_RANK', 'USG%_RANK', 'EFG%_RANK']


if st.button(f'Show All {player} Data'):
    # show all the data with no scroll bar
    st.dataframe(player_df, use_container_width=True, hide_index=True)
    st.button('Hide Data', key=f'hide_{player}_data')
# an interesting alternate idea (or maybe concurrent) is to basically make the website a scrolling timeline of the player: Kind of like the spotify wrapped, but a timeline of the player with 
# their most important stats and their overall impact on the game? Would some sort of impact on the game metric be interesting? How would I define that just using stats?
# I think I have to start with the most impactful players: Steph is an outlier in 3pt shooting all time. But whenever it started (so he has a large difference in 3PAs to how quickly it gets closer)
# could look at something like that? As if the player is a trendsetter if they are an outlier in a stat and the rest of the league (or at least a certain number of players follows suit?)
