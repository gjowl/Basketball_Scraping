import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import create_year_data_dict

# SET PAGE CONFIG
st.set_page_config(page_title='Yearly Plots',
                   page_icon='',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Yearly Plots')

# VARIABLES 
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
#datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD'
colors = '/mnt/d/github/Basketball_Scraping/site/team_colors_hex.csv'
options = '/mnt/d/github/Basketball_Scraping/site/options.csv'

# HARDCODED STAT GROUPS
threes = ['3PM_PG', '3PA_PG', '3P%']
twos = ['2PM_PG', '2PA_PG', '2P%']
fgs = ['FGM_PG', 'FGA_PG', 'FG%']
fts = ['FTM_PG', 'FTA_PG', 'FT%']
general = ['APG', 'RPG', 'DREB_PG', 'OREB_PG', 'TOV_PG', 'SPG', 'BPG', 'PF_PG']
advanced = ['AST_TO', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%']

# READ IN THE TEAM COLORS
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

# MAIN
# TODO: might it be interesting to only look at specific teams?
# TODO: figure out what might be interesting here, or may have to bail on it for now
# TODO: st.multiselect, st.pills may be a good tool to use for the comparing stats
## PAGE SETUP BELOW
## TOGGLE FOR TRADITIONAL/ADVANCED STATS
## SELECT THE NUMBER OF YEARS
## SELECT THE NUMBER OF GAMES PLAYED
## SELECT THE MAXIMUM NUMBER OF PLAYERS TO PLOT
## SELECT THE STAT TO PLOT
## PLOTS
# st.progress, st.spinner, st.status might be good tools for loading times

# if you were to make this kind of like an interactive walkthrough; populating the page for each person being added would be helpful
# I think making this an interactive page is for the best!
# Let people pick the stat they want to see against year
# make it so that you can make up to 3 (?) simultaneously

## TOGGLE FOR TRADITIONAL/ADVANCED STATS
if st.toggle('**Advanced**'):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'

## traverse directory to load data
year_data_dict = create_year_data_dict(datadir)

## get all the unique player names from the year_data_dict
player_names = pd.DataFrame()
for key in year_data_dict.keys():
    # add the year column to the dataframe
    year_df = year_data_dict[key]
    year_df['YEAR'] = key
    player_names = pd.concat([player_names, year_df], ignore_index=True)
    
# check if the player name is duplicated, if so remove the duplicates
player_names_no_dups = player_names['PLAYER_NAME'].drop_duplicates(keep=False)

# if the player is in the list, remove them from the dataframe
player_names = player_names[~player_names['PLAYER_NAME'].isin(player_names_no_dups)]
player_names = player_names.reset_index(drop=True)
# count the number of instances of the player names in the dataframe
player_names_count = player_names['PLAYER_NAME'].value_counts()

## SELECT THE NUMBER OF YEARS
# add an input slider for the number of years to filter by
count = st.slider('*Select the number of years to filter by*', 1, 10, 5) 
player_names_count = player_names_count[player_names_count > 10]
player_names = player_names[player_names['PLAYER_NAME'].isin(player_names_count.index)]
#st.write(len(player_names), ' players that have more than 5 years of data in the league')

## SELECT THE NUMBER OF GAMES PLAYED
# TODO: might be interesting to do some kind of density plot of GP
games_played = st.slider('*Select the number of games played to filter by*', 1, 82, 20) # 82 is the max number of games played in a season
player_names = player_names[player_names['GP'] > games_played]

## SELECT THE MAXIMUM NUMBER OF PLAYERS TO PLOT
# TODO: might not need this?
num_players = st.slider('*Select the maximum number of players to plot per year*', 1, 100, 50)
st.divider()

## CHOOSE THE STAT TO PLOT
# make a search bar for the stats to plot
stat = st.selectbox('**Select the stat to plot**', player_names.columns[3:]) # from the GP column and on
# keep only the players with the top 100 of the stat for each year
player_names = player_names.sort_values(by=stat, ascending=False).groupby('YEAR').head(num_players)
# sort the players by year
player_names = player_names.sort_values(by='SEASON')

# add a short wait here (checking stat type...) (make it feel like an old school kind of vibe (that can be toggled))
if stat in threes:
    attempts = st.slider('*Select the minimum number of 3PA_PG to filter by*', 1, 10, 2) 
    player_names = player_names[player_names['3PA_PG'] > attempts]
if stat in twos:
    attempts = st.slider('*Select the minimum number of 2PA_PG to filter by*', 1, 10, 2) 
    player_names = player_names[player_names['2PA_PG'] > attempts]
if stat in general:
    max_stat = int(player_names[stat].max())
    attempts = st.slider(f'*Select the minimum number of **{stat}** to filter by*', 1, max_stat, 2)
    player_names = player_names[player_names[stat] > attempts]
# make boxplots for each year
#fig = px.box(player_names, x='SEASON', y=stat, color='PLAYER_NAME', hover_name='PLAYER_NAME', title=f'{stat} vs YEAR')
#fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
#fig.update_layout(showlegend=False)
#st.plotly_chart(fig, use_container_width=True)

#fig = px.scatter(player_names, x='SEASON', y=stat, color='PLAYER_NAME', hover_name='PLAYER_NAME', title=f'{stat} vs YEAR')
#fig.update_layout(showlegend=False)
## TODO: these might actually just be better as yearly boxplots; maybe add a button to toggle between the two?
#st.plotly_chart(fig, use_container_width=True)

traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'TOV_PG', 'PF_PG']

#    # trace a line between all values that have the same PLAYER_NAME
#    # another idea: get the biggest movers from year to year to identify players that were starting to space out the league at the 4 and 5 positions
## TODO: draw a line between the points of the same player