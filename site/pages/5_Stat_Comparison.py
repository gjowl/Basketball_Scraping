import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import set_axis_text

# SET PAGE CONFIG
st.set_page_config(page_title='Player Stat Comparison',
                   page_icon='🔍',
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

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

# Functions
def compare_player_scatterplot(_playerdf_1, _playerdf_2, _xaxis, _yaxis, n=0):
    pname_1, pname_2= _playerdf_1['PLAYER_NAME'].values[0], _playerdf_2['PLAYER_NAME'].values[0]
    # make the hover template for the player name
    if _yaxis != 'GP':
        hover_template_1 = pname_1 + f'<br>{_xaxis}: ' + _playerdf_1[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + _playerdf_1[_yaxis].astype(str) + '<br>GP: ' + _playerdf_1['GP'].astype(str)
        hover_template_2 = pname_2 + f'<br>{_xaxis}: ' + _playerdf_2[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + _playerdf_2[_yaxis].astype(str) + '<br>GP: ' + _playerdf_2['GP'].astype(str)
    else:
        hover_template_1 = pname_1 + f'<br>{_xaxis}: ' + _playerdf_1[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + _playerdf_1[_yaxis].astype(str)
        hover_template_2 = pname_2 + f'<br>{_xaxis}: ' + _playerdf_2[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + _playerdf_2[_yaxis].astype(str)
    
    # make a scatterplot of the 3P% vs year for both players on the same graph
    fig = px.scatter(_playerdf_1, x=_xaxis, y=_yaxis, color='PLAYER_NAME', hover_name='PLAYER_NAME')
    # add in the hover template for the first player
    fig.add_trace(go.Scatter(x=_playerdf_1[_xaxis], y=_playerdf_1[_yaxis], mode='markers', name=player_name, hovertemplate=hover_template_1, marker=dict(color='blue', size=10, line=dict(width=2, color='DarkSlateGrey'))))
    fig.add_trace(go.Scatter(x=_playerdf_1[_xaxis], y=_playerdf_1[_yaxis], mode='lines', name=player_name, line=dict(color='blue', width=2)))

    # add the second player to the graph
    fig.add_trace(go.Scatter(x=_playerdf_2[_xaxis], y=_playerdf_2[_yaxis], mode='markers', name=player_name_2, hovertemplate=hover_template_2, marker=dict(color='red', size=10, line=dict(width=2, color='DarkSlateGrey'))))
    fig.add_trace(go.Scatter(x=_playerdf_2[_xaxis], y=_playerdf_2[_yaxis], mode='lines', name=player_name_2, line=dict(color='red', width=2)))

    fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
    # remove the legend
    fig.update_layout(showlegend=False)
    fig.update_layout(title=f'{_yaxis} per {_xaxis}', xaxis_title=_xaxis, yaxis_title=_yaxis)
    st.plotly_chart(fig, key=f'compare_player_scatterplot_{n}', use_container_width=True)

# MAIN
## PAGE SETUP BELOW
st.write('This page allows you to compare the stats of two players over the years they have played in the league.')




# stolen from yearly; could maybe make a function?
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
    
# initial filtering
player_names['SEASON'] = player_names['YEAR'].str.split('-').str[0]
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

# choose a player from the list of players
c1, c2 = st.columns(2)
with c1:
    st.write('**Choose a player**')
    # set the default to Stephen Curry
    player_name = st.selectbox('Player 1', player_names_count.index.tolist(), index=player_names_count.index.tolist().index('Stephen Curry'),key='player_name')
with c2:
    st.write('**Choose a player to compare**')
    # set the default to Steve Nash
    player_name_2 = st.selectbox('Player 2', player_names_count.index.tolist(), key='player_name_2', index=player_names_count.index.tolist().index('Steve Nash'))

# get the data for the selected player
player_data = player_names[player_names['PLAYER_NAME'] == player_name].reset_index(drop=True)
player_data_2 = player_names[player_names['PLAYER_NAME'] == player_name_2].reset_index(drop=True)

# 
st.divider()

# if the same player is chosen, show the selectbox again for years
# TODO: choose what to do if the same player is chosen
if player_name == player_name_2:
    st.write('Same player chosen, please choose a different player')
else:
    # plot the data against each other on the same plot
    st.write('*Choose up to 3 stats to compare*')
    #fig = make_year_scatterplot(player_data, '3P%', team_colors, True)
    # TODO: add in recommended stats to compare
    # TODO: decide if I should get some averages for each player? Or average overall for all players throughout the years both players played?
    # TODO: is there a way to compare Westbrook's late and early stage career? Could be interesting to see clearly hwo he's the same and has changed
    # choose a stat to compare
    stat_1 = st.selectbox('*Stat 1*', player_data.columns.tolist()[3:], key='stat_1', index=player_data.columns.tolist()[3:].index('PPG'))
    stat_2 = st.selectbox('*Stat 2*', player_data_2.columns.tolist()[3:], key='stat_2', index=player_data_2.columns.tolist()[3:].index('3P%'))
    stat_3 = st.selectbox('*Stat 3*', player_data_2.columns.tolist()[3:], key='stat_3', index=player_data_2.columns.tolist()[3:].index('FG%'))
    stats = [stat_1, stat_2, stat_3]

    # variables
    if st.toggle('**Compare by years in league**', key='compare_years', value=True):
        xaxis = 'YEARS_IN_LEAGUE'
        # get the years in league for each player
        player_data['YEARS_IN_LEAGUE'] = player_data['SEASON'].astype(int) - player_data['SEASON'].astype(int).min()
        player_data_2['YEARS_IN_LEAGUE'] = player_data_2['SEASON'].astype(int) - player_data_2['SEASON'].astype(int).min()
        cols = ['PLAYER_NAME', 'YEARS_IN_LEAGUE', 'GP', stat_1, stat_2, stat_3]
    else:
        xaxis = 'SEASON'
        cols = ['PLAYER_NAME', 'SEASON', 'GP', stat_1, stat_2, stat_3]

    st.write('By default data are plotted by season, but you can also choose to plot by years in the league by switching the toggle above.')
    # keep the first 3 columns and the stat columns
    player_data, player_data_2 = player_data[cols], player_data_2[cols]
    
    # plot the data
    n = 0
    for stat in stats:
        compare_player_scatterplot(player_data, player_data_2, xaxis, stat, n)
        n+=1

    # add a button to show the player data
    if st.button('Show player data', key='show_player_data'):
        c1, c2 = st.columns(2)
        with c1:
            st.write('Player 1')
            st.dataframe(player_data, use_container_width=True, hide_index=True)
        with c2:
            st.write('Player 2')
            st.dataframe(player_data_2, use_container_width=True, hide_index=True)
        st.button('Hide player data', key='hide_player_data')