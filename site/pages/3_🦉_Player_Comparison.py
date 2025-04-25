import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import create_year_data_dict

# SET PAGE CONFIG
st.set_page_config(page_title='Player Comparison',
                   page_icon='🦉',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Player Comparison Page')

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
advanced = False

# READ IN THE TEAM COLORS
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

# FUNCTIONS
def compare_player_scatterplot(_player_dfs, _xaxis, _yaxis, n=0):
    names, hover_templates = [], []
    for player_df in _player_dfs:
        names.append(player_df['PLAYER_NAME'].values[0])
    # make the hover template for the player name
    if _yaxis != 'GP':
        for player_df, name in zip(player_dfs, names):
            hover_template = name + f'<br>{_xaxis}: ' + player_df[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + player_df[_yaxis].astype(str) + '<br>GP: ' + player_df['GP'].astype(str)
            hover_templates.append(hover_template)
    else:
        for player_df, name in zip(player_dfs, names):
            hover_template = name + f'<br>{_xaxis}: ' + player_df[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + player_df[_yaxis].astype(str)
            hover_templates.append(hover_template)
    # make a scatterplot of the 3P% vs year for both players on the same graph
    #fig = px.scatter(player_dfs[0], x=_xaxis, y=_yaxis, color='PLAYER_NAME', hover_name='PLAYER_NAME')
    #fig.add_trace(go.Scatter(x=player_dfs[0][_xaxis], y=player_dfs[0][_yaxis], mode='lines', name=player_name, hovertemplate=hover_template, marker=dict(color='white', size=18, line=dict(width=2, color='DarkSlateGrey'))))
    #fig.add_trace(go.scatter(x=player_dfs[0][_xaxis], y=player_dfs[0][_yaxis], mode='lines', name=player_name, line=dict(color='#f27522', width=2)))
    for player_df, hover_template, player_name in zip(_player_dfs, hover_templates, names):
        # if the first player, create the fig
        if player_df['PLAYER_NAME'].values[0] == player_dfs[0]['PLAYER_NAME'].values[0]:
            fig = px.scatter(player_df, x=_xaxis, y=_yaxis, color='PLAYER_NAME', hover_name='PLAYER_NAME')
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='lines', name=player_name, hovertemplate=hover_template, marker=dict(color='white', size=18, line=dict(width=2, color='DarkSlateGrey'))))
        else:
            # add in the hover template for the first player
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='markers', name=player_name, hovertemplate=hover_template, marker=dict(color='white', size=18, line=dict(width=2, color='DarkSlateGrey'))))
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='lines', name=player_name, hovertemplate=hover_template, marker=dict(color='white', size=18, line=dict(width=2, color='DarkSlateGrey'))))
    ## add the second player to the graph
    #fig.add_trace(go.Scatter(x=_playerdf_2[_xaxis], y=_playerdf_2[_yaxis], mode='markers', name=player_name_2, hovertemplate=hover_template_2, marker=dict(color='#F27522', size=18, line=dict(width=2, color='DarkSlateGrey'))))
    #fig.add_trace(go.scatter(x=_playerdf_2[_xaxis], y=_playerdf_2[_yaxis], mode='lines', name=player_name_2, line=dict(color='#f27522', width=2)))
    fig.update_traces(marker=dict(size=16, line=dict(width=3, color='black')))
    # remove the legend
    fig.update_layout(showlegend=False)
    fig.update_layout(title=f'{_yaxis} per {_xaxis}', xaxis_title=_xaxis, yaxis_title=_yaxis)
    st.plotly_chart(fig, key=f'compare_player_scatterplot_{n}', use_container_width=True)

# INITIAL DATA PROCESSING
year_data_dict = create_year_data_dict(datadir)

## GET ALL THE UNIQUE PLAYER NAMES FROM THE YEAR_DATA_DICT
player_names = pd.DataFrame()
for key in year_data_dict.keys():
    # add the year column to the dataframe
    year_df = year_data_dict[key]
    year_df['YEAR'] = key
    player_names = pd.concat([player_names, year_df], ignore_index=True)
    
# check if the player name is duplicated, if so remove the duplicates
player_names_no_dups = player_names['PLAYER_NAME'].drop_duplicates(keep=False)
#st.write(len(player_names_no_dups), ' players that only have 1 year of data in the league')
# if the player is in the list, remove them from the dataframe
#player_names = player_names[player_names['PLAYER_NAME'].isin(player_names_no_dups)]
player_names = player_names[~player_names['PLAYER_NAME'].isin(player_names_no_dups)]
# reset the index of the dataframe
player_names = player_names.reset_index(drop=True)
# count the number of instances of the player names in the dataframe
player_names_count = player_names['PLAYER_NAME'].value_counts()

# MAIN
## PAGE SETUP BELOW
## PAGE BLURB
## TOGGLE FOR TRADITIONAL/ADVANCED STATS
## SELECT PLAYERS
## TOGGLE TO PLOT BY YEARS IN LEAGUE OR SEASON
## SELECT STATS TO PLOT
## PLOTS

## PAGE BLURB
st.write('This page allows you to compare the stats of two players over the years they have played in the league since the 1996-97 season (as far back as nba.com has data).')
# TODO: add a bit more a blurb here for the page
st.divider()

## TOGGLE FOR TRADITIONAL/ADVANCED STATS
st.write('**Toggle below to switch between traditional/advanced stats**')
if st.toggle('**Advanced Stats**'):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
    advanced = True

# SELECT PLAYERS
# TODO: is it possible to add a list of recommended players to compare? Like a list of players that are similar to the player chosen
# TODO: write a way that outputs the most important takeaway from the data
# choose a player from the list of players
players = st.multiselect('**Select players to compare**', player_names_count.index.tolist(), default=['Stephen Curry', 'Steve Nash'], key='players')

# get the data for the selected player
player_dfs = []
for player in players:
    player_df = player_names[player_names['PLAYER_NAME'] == player].reset_index(drop=True)
    player_dfs.append(player_df)
st.divider()

## TOGGLE TO PLOT BY YEARS IN LEAGUE OR SEASON
if st.toggle('**Compare by years in league**', key='compare_years', value=True):
    xaxis = 'YEARS_IN_LEAGUE'
    for player_df in player_dfs:
        # get the years in league for each player
        player_df['YEARS_IN_LEAGUE'] = player_df['SEASON'].astype(int) - player_df['SEASON'].astype(int).min()
else:
    xaxis = 'SEASON'

# SELECT STATS TO PLOT 
# TODO: choose what to do if the same player is chosen
# TODO: add in recommended stats to compare
# TODO: decide if I should get some averages for each player? Or average overall for all players throughout the years both players played?
cols = []
# plot the data against each other on the same plot
st.write('*Choose up to 3 stats to compare*')
# choose a stat to compare
if advanced == False:
    stat_1 = st.selectbox('*Stat 1*', player_dfs[0].columns.tolist()[3:], key='stat_1', index=player_dfs[0].columns.tolist()[3:].index('PPG'))
    stat_2 = st.selectbox('*Stat 2*', player_dfs[0].columns.tolist()[3:], key='stat_2', index=player_dfs[0].columns.tolist()[3:].index('3P%'))
    stat_3 = st.selectbox('*Stat 3*', player_dfs[0].columns.tolist()[3:], key='stat_3', index=player_dfs[0].columns.tolist()[3:].index('FG%'))
    cols = ['PLAYER_NAME', xaxis, 'GP', stat_1, stat_2, stat_3]
else:
    stat_1 = st.selectbox('*Stat 1*', player_dfs[0].columns.tolist()[3:], key='stat_1', index=player_dfs[0].columns.tolist()[3:].index('TS%'))
    stat_2 = st.selectbox('*Stat 2*', player_dfs[0].columns.tolist()[3:], key='stat_2', index=player_dfs[0].columns.tolist()[3:].index('USG%'))
    stat_3 = st.selectbox('*Stat 3*', player_dfs[0].columns.tolist()[3:], key='stat_3', index=player_dfs[0].columns.tolist()[3:].index('AST%'))
    cols = ['PLAYER_NAME', xaxis, 'GP', stat_1, stat_2, stat_3]
stats = [stat_1, stat_2, stat_3]
st.divider()

# keep the first 3 columns and the stat columns
final_dfs = []
for player_df in player_dfs:
    player_df = player_df[cols]
    final_dfs.append(player_df)

# PLOTS
n = 0
for stat in stats:
    compare_player_scatterplot(final_dfs, xaxis, stat, n)
    n+=1

# add a button to show the player data
if st.button('Show player data', key='show_player_data'):
    c1, c2 = st.columns(2)
    with c1:
        st.write(f'{player_name}')
        st.dataframe(player_data, use_container_width=True, hide_index=True)
    with c2:
        st.write(f'{player_name_2}')
        st.dataframe(player_data_2, use_container_width=True, hide_index=True)
    st.button('Hide player data', key='hide_player_data')

## Some fun player comparison examples that you NEED to be able to do for this website to work out:
## - Nash vs Steph
## - MKG vs Haywood Highsmith
## - Matas vs Tatum (from his first year with the type of game he has (percentages and usage and advanced might agree?); let's see if he adds the mid-range and passing next!)
## - Daniel Gafford vs Gary Payton II