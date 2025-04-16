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
player_names = pd.Series()
for key in year_data_dict.keys():
    player_names = pd.concat([player_names, year_data_dict[key]['PLAYER_NAME']])
player_names = player_names.unique()


all_data = pd.DataFrame()
fig = go.Figure()
# loop through the year_data_dict
for key in year_data_dict.keys():
    # get the data for the player from all years they played in the league
    year_df = year_data_dict[key]
    # add a year column to the dataframe
    year_df['YEAR'] = key
    # scatterplot the data
    # keep the top 100 players by 3PM_PG
    year_df = year_df.sort_values(by='3PM_PG', ascending=False).head(20)
    fig.add_trace(go.Scatter(x=year_df['YEAR'], y=year_df['3PA_PG'], mode='markers', name=key, hovertemplate='%{text}', text=year_df['PLAYER_NAME']))
    # change to the color 1 for each point
    fig.update_traces(marker=dict(size=10, color=year_df['Color 1']), selector=dict(mode='markers'))
# TODO: draw a line between the points of the same player
st.plotly_chart(fig, use_container_width=True)
