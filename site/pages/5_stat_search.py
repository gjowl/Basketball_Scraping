import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go

# SET PAGE CONFIG
st.set_page_config(page_title='Comparison Stats',
                   page_icon='',
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

# FUNCTIONS
# loop through the year_data_dictionary and get all the data for the player
def get_player_data(_year_data_dict, _player):
    output_df = pd.DataFrame()
    for key in _year_data_dict.keys():
        # get the data for the player
        tmp_df = _year_data_dict[key][_year_data_dict[key]['PLAYER_NAME'] == _player]
        # check if the dataframe is empty, if so skip it
        if tmp_df.empty:
            continue
        # add the year to the dataframe
        tmp_df['YEAR'] = key
        output_df = pd.concat([output_df, tmp_df], axis=0)
        # move year to the front of the dataframe
        output_df = output_df[['YEAR'] + [col for col in output_df.columns if col != 'YEAR']]
        # replace the index column with the year column
        output_df = output_df.reset_index(drop=True)
    return output_df

def update_yaxis(_fig, _data, _col):
    min = _data[_col].min()
    max = _data[_col].max()
    min = round(min, 1) - 0.05
    max = round(max, 1) + 0.05
    _fig.update_yaxes(range=[min, max])

def change_to_team_colors(_fig, _data, team_colors):
    # set the color for each player to be the same as their team color
    for i in range(len(_data)):
        # get the team abbreviation and match it to the hexcolors file
        team = _data['TEAM_ABBREVIATION'][i]
        # get the color from the team_colors file
        color = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
        _fig.data[i].marker.color = color

# MAIN
## PAGE SETUP BELOW
## TODO: add in the setup of the page details here

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

# get all the unique player names from the year_data_dict
player_names = pd.Series()
for key in year_data_dict.keys():
    player_names = pd.concat([player_names, year_data_dict[key]['PLAYER_NAME']])
player_names = player_names.unique()

# create a search bar for the player names
player = st.selectbox('Select the player to load', player_names)
# below doesn't work; need to think of an alternative
#file2 = st.selectbox('Select the year of interest', list(year_data_dict1.keys()))
#player2 = st.selectbox('Select the player to load', list(year_data_dict[file1]['PLAYER_NAME'].unique()))
#player = st_searchbox(year_data_dict[file1]['PLAYER_NAME'].unique(), label='Search for a player', placeholder='Search for a player', key='player_searchbox', default_value='')

# get the data for the player from all years they played in the league
player_df = get_player_data(year_data_dict, player)
if st.button('Show Data'):
    st.write(player_df)
    st.button('Hide Data')

# TODO: add in a st.toggle here to show different versions of data (ex. turning on/off gp threshold)
name_and_year = ['PLAYER_NAME', 'YEAR']
#percent = ['FG%', '2P%', '3P%', 'FT%']
percent = ['FG%', '2P%', '3P%']
shots = ['FGA_PG', 'FGM_PG', '2PA_PG', '2PM_PG', '3PA_PG', '3PM_PG', 'FTA_PG', 'FTM_PG'] # make into quadrant plots
traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'TOV_PG', 'PF_PG'] # unsure yet
#advanced = ['AST_TO', 'NBA_FANTASY_PTS_PG', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'STL%', 'BLK%']
# keep all the shooting stats and player name and year
percent_df = player_df[name_and_year + percent]
# remove the part after the - from year
#percent_df['YEAR'] = percent_df['YEAR'].str.split('-').str[0]
shots_df = player_df[name_and_year + shots]
traditional_df = player_df[name_and_year + traditional]

# list of tabs
tab1, tab2, tab3 = st.tabs(['Percent', 'Shooting', 'Traditional'])
with tab1:
    st.header('Percent Stats')
    if st.button('Show Percent Data'):
        st.write('Below are the shooting percentages for the player')
        st.write(percent_df)
        st.button('Hide Percent Data')
    fig_list = []
    # plot a box plot with the points overlaid for each stat
    fig = go.Figure()
    for stat in percent:
        # make a array of the stat with the same size as the percent_df
        x = [stat] * len(percent_df[stat])
        # create a hover label with the year and the stat value
        hover_label = [f'{year}: {value}' for year, value in zip(percent_df['YEAR'], percent_df[stat])]
        fig.add_trace(go.Box(y=percent_df[stat], x=x, name=stat, boxmean='sd', line_color='orange', marker_color='orange', hoverinfo='text', hovertext=hover_label, boxpoints='all', pointpos=0, opacity=0.5, showlegend=False))
        # replace the hover label w/ the {YEAR}: {percentage} to the points
        fig.update_traces(marker=dict(size=7, color='white', line=dict(width=3, color='white')))
    st.plotly_chart(fig, use_container_width=True)
# currently just hardcoding; but I think I should try to find a better way to do the above?
with tab2:
    st.header('Shooting Stats')
    if st.button('Show Shooting Data'):
        st.write('Below are the shooting stats for the player')
        st.write(shots_df)
        st.button('Hide Shooting Data')
    # get the difference between the FGA and FGM for each year 
    fig = px.scatter(player_df, x='FGM_PG', y='FGA_PG', color='YEAR', hover_name='TEAM_ABBREVIATION', title=f'{player} Shooting Stats')
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='black')))
    fig.update_layout(xaxis_title='FGM', yaxis_title='FGA')
    # update the color of the points to be the same as the team color
    change_to_team_colors(fig, player_df, team_colors)
    st.plotly_chart(fig, use_container_width=True)
    # add a way to change the color if too close
with tab3:
    st.header('Traditional Stats')
    st.write('Below are the traditional stats for the player')
    st.write(player_df[name_and_year + traditional])
    # here I think having that player as a point within all players (similar to the quadrant plots) might work well
    # add a dropdown to select the season of interest

# TODO: st.multiselect, st.pills may be a good tool to use for the comparing stats