import streamlit as st
import os, pandas as pd
import plotly.express as px
from streamlit_searchbox import st_searchbox


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

year_data_dict1 = year_data_dict.copy()
c1, c2 = st.columns(2)
# create a search bar of all the filenames in the directory
with c1:
    file1 = st.selectbox('Select the year of interest', list(year_data_dict.keys()))
with c2:
    player = st.selectbox('Select the player to load', list(year_data_dict[file1]['PLAYER_NAME'].unique()))
# below doesn't work; need to think of an alternative
#file2 = st.selectbox('Select the year of interest', list(year_data_dict1.keys()))
#player2 = st.selectbox('Select the player to load', list(year_data_dict[file1]['PLAYER_NAME'].unique()))
#player = st_searchbox(year_data_dict[file1]['PLAYER_NAME'].unique(), label='Search for a player', placeholder='Search for a player', key='player_searchbox', default_value='')
# output the player stats
st.write(year_data_dict[file1][year_data_dict[file1]['PLAYER_NAME'] == player])

# get the data for the player from all years they played in the league
player_df = get_player_data(year_data_dict, player)

st.write(player_df)
# TODO: separate into tabs for each of the stats
name_and_year = ['PLAYER_NAME', 'YEAR']
percent = ['FG%', '3P%', 'FT%']
shots = ['FG%', 'FGA_PG', 'FTA_PG', '2P%', '2PA_PG', '2PM_PG', '3P%', '3PA_PG', '3PM_PG', 'PF_PG']
traditional = ['MPG', 'PTS', 'AST', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'TOV_PG']
#advanced = ['AST_TO', 'NBA_FANTASY_PTS_PG', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'STL%', 'BLK%']
# keep all the shooting stats and player name and year
percent_df = player_df[name_and_year + percent]
#if st.button('All Data', key='all_data_button'):
#    st.write(output_df)
#    st.button('Hide')
