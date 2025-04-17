import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import change_to_team_colors, plot_quadrant_scatter, get_player_data, get_player_ranks, create_player_rank_bar_graph, set_axis_text, adjust_axes

# SET PAGE CONFIG
st.set_page_config(page_title='Stat Search',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Welcome to the stat search page!')

# VARIABLES 
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
#datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
#contains = 'all_game' # file you want to read
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD'
contains = '2023-24_boxscore' # file you want to read
colors = '/mnt/d/github/Basketball_Scraping/site/team_colors_hex.csv'
options = '/mnt/d/github/Basketball_Scraping/site/options.csv'

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

# MAIN
## PAGE SETUP BELOW


## traverse directory to load data
year_data_dict = {}
for root, dirs, files in os.walk(datadir):
    for file in files:
        # look if the name of the file is what you want
        # read in the file
        tmp_df = pd.read_csv(os.path.join(root, file))
        # get the filename and remove the extension, separate by _
        filename = file.split('_')[0]
        # check if ~ is in the filename, if so don't add it to the dictionary
        if '~' in filename:
            continue
        # add the df to the dictionary with the filename as the key
        year_data_dict[filename] = tmp_df

## get all the unique player names from the year_data_dict
player_names = pd.DataFrame()
for key in year_data_dict.keys():
    # add the year column to the dataframe
    year_df = year_data_dict[key]
    year_df['YEAR'] = key
    player_names = pd.concat([player_names, year_df], ignore_index=True)
    
# check if the player name is duplicated, if so remove the duplicates
player_names_no_dups = player_names['PLAYER_NAME'].drop_duplicates(keep=False)
st.write(len(player_names_no_dups), ' players that only have 1 year of data in the league')
# if the player is in the list, remove them from the dataframe
#player_names = player_names[player_names['PLAYER_NAME'].isin(player_names_no_dups)]
player_names = player_names[~player_names['PLAYER_NAME'].isin(player_names_no_dups)]
# reset the index of the dataframe
player_names = player_names.reset_index(drop=True)
# count the number of instances of the player names in the dataframe
player_names_count = player_names['PLAYER_NAME'].value_counts()
# keep the players that have more than 5 instance in the dataframe

# initial filtering
player_names['SEASON'] = player_names['YEAR'].str.split('-').str[0]
# add an input slider for the number of years to filter by
count = st.slider('Select the number of years to filter by', 1, 10, 5) 
# remove the players that have less than 10 years of data
player_names_count = player_names_count[player_names_count > 10]
player_names = player_names[player_names['PLAYER_NAME'].isin(player_names_count.index)]
st.write(len(player_names), ' players that have more than 5 years of data in the league')
# do some initial filtering
games_played = st.slider('Select the number of games played to filter by', 1, 82, 20) # 82 is the max number of games played in a season
player_names = player_names[player_names['GP'] > games_played]
# TODO: might be interesting to do some kind of density plot of GP
# make a search bar for the stats to plot
stat = st.selectbox('Select the stat to plot', player_names.columns[3:]) # from the GP column and on

# add a slider for the number of players to plot per year
num_players = st.slider('Select the number of players to plot per year', 1, 100, 50)

# keep only the players with the top 100 of the stat for each year
player_names = player_names.sort_values(by=stat, ascending=False).groupby('YEAR').head(num_players)

# sort the players by year
player_names = player_names.sort_values(by='SEASON')
# plot the stat against YEAR
# 3pt stats
threes = ['3PM_PG', '3PA_PG', '3P%']
twos = ['2PM_PG', '2PA_PG', '2P%']
fgs = ['FGM_PG', 'FGA_PG', 'FG%']
fts = ['FTM_PG', 'FTA_PG', 'FT%']
general = ['APG', 'RPG', 'DREB_PG', 'OREB_PG', 'TOV_PG', 'SPG', 'BPG', 'PF_PG']
# add a short wait here (checking stat type...) (make it feel like an old school kind of vibe (that can be toggled))
# if the stat is in threes, add a slider for the number of 3PA to filter by
if stat in threes:
    attempts = st.slider('Select the minimum number of 3PA_PG to filter by', 1, 10, 2) # 82 is the max number of games played in a season
    player_names = player_names[player_names['3PA_PG'] > attempts]
    # make sure the 3PA is more than 
if stat in twos:
    attempts = st.slider('Select the minimum number of 2PA_PG to filter by', 1, 10, 2) # 82 is the max number of games played in a season
    player_names = player_names[player_names['2PA_PG'] > attempts]
if stat in general:
    # get the max of the stat rounded down
    max_stat = int(player_names[stat].max())
    attempts = st.slider(f'Select the minimum number of {stat} to filter by', 1, max_stat, 2) # 82 is the max number of games played in a season
    player_names = player_names[player_names[stat] > attempts]
fig = px.scatter(player_names, x='SEASON', y=stat, color='PLAYER_NAME', hover_name='PLAYER_NAME', hover_data=['3PM_PG'], title=f'{stat} vs YEAR')
st.plotly_chart(fig, use_container_width=True)
# if you were to make this kind of like an interactive walkthrough; populating the page for each person being added would be helpful

# I think making this an interactive page is for the best!
# Let people pick the stat they want to see against year
# make it so that you can make up to 3 (?) simultaneously

traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'TOV_PG', 'PF_PG']

#    # trace a line between all values that have the same PLAYER_NAME
#
#    # another idea: get the biggest movers from year to year to identify players that were starting to space out the league at the 4 and 5 positions
## TODO: draw a line between the points of the same player
## Some fun player comparison examples that you NEED to be able to do for this website to work out:
## - Nash vs Steph
## - MKG vs Haywood Highsmith
## - Matas vs Tatum (from his first year with the type of game he has (percentages and usage and advanced might agree?); let's see if he adds the mid-range and passing next!)
#st.plotly_chart(fig, use_container_width=True)
