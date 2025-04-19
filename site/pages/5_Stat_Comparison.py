import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go

# SET PAGE CONFIG
st.set_page_config(page_title='Stat Comparison',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Welcome to the stat comparison page!')

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
    st.write('Choose a player')
    player_name = st.selectbox('Player Name', player_names_count.index.tolist(), key='player_name')
with c2:
    st.write('Choose a player to compare')
    player_name_2 = st.selectbox('Player Name', player_names_count.index.tolist(), key='player_name_2')

# get the data for the selected player
player_data = player_names[player_names['PLAYER_NAME'] == player_name].reset_index(drop=True)
player_data_2 = player_names[player_names['PLAYER_NAME'] == player_name_2].reset_index(drop=True)

# if the same player is chosen, show the selectbox again for years
# TODO: choose what to do if the same player is chosen
if player_name == player_name_2:
    st.write('Same player chosen, please choose a different player')
else:
    # plot the data against each other on the same plot
    st.write('Plotting the data against each other')
    #fig = make_year_scatterplot(player_data, '3P%', team_colors, True)
    # TODO: add in recommended stats to compare
    # TODO: allow for more than just 1 stat
    # choose a stat to compare
    stat = st.selectbox('Stat to compare', player_data.columns.tolist()[3:], key='stat')

    # make a scatterplot of the 3P% vs year for both players on the same graph
    fig = px.scatter(player_data, x='SEASON', y=stat, color='PLAYER_NAME', hover_name='PLAYER_NAME')
    fig.add_trace(go.Scatter(x=player_data['SEASON'], y=player_data[stat], mode='lines', name=player_name, line=dict(color='blue', width=2)))

    # add the second player_data_2
    fig.add_trace(go.Scatter(x=player_data_2['SEASON'], y=player_data_2[stat], mode='markers', name=player_name_2))
    fig.add_trace(go.Scatter(x=player_data_2['SEASON'], y=player_data_2[stat], mode='lines', name=player_name_2, line=dict(color='red', width=2)))
    # add the first player_data
    fig.update_traces(marker=dict(size=12,
                            line=dict(width=2,
                                      color='DarkSlateGrey')))
    # remove the legend
    fig.update_layout(showlegend=False)

    fig.update_layout(title=f'{stat} vs Year', xaxis_title='Year', yaxis_title=stat)
    st.plotly_chart(fig)