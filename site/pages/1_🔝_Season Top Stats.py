import streamlit as st
import os, pandas as pd
import plotly.express as px
from functions import sort_and_show_data, plot_quadrant_scatter

# SET PAGE CONFIG
st.set_page_config(page_title='Top Stats',
                   page_icon='🔝',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Welcome to the top stats page!')

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
# changes the figure to the team colors

# MAIN
## PAGE SETUP BELOW
'''
 - Select the number of players to show 
 - Select the number of games played
 - Select the stat to plot
 - Plots
'''
## TODO: add in the setup of the page details here
## TODO: fix the blurb at the top of the page
## TODO: add in a season picker
## STATS TO GET
stats = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 

## add in sliders for the number of players and games played
num_players = st.slider('*Number of players to show*', 1, 30, 10)
num_gp = st.slider('*Minimum number of games played*', 1, 82, 25)

## add in a text box to search for a player
st.write(f'Below you can click to view data for the top {num_players} players over the last {num_gp} games played in various statistical categories.')
st.write(f'All data sourced from https://www.nba.com/stats/leaders')
st.divider()

## traverse directory to load data
for root, dirs, files in os.walk(datadir):
    for file in files:
        # look if the name of the file is what you want
        if contains in file:
            datafile = os.path.join(root, file)
            data = pd.read_csv(datafile)


## SELECTION BOX TO CHOOSE A STAT TO VIEW
option = st.selectbox(
    'Select a stat to view the stats',
    stats,
    index=0
)

# get the sort column name from the options file
sort_col = option_df[option_df['OPTION'] == option]['SORT'].values[0]

## SIMPLE FILTERING/DATA PREPROCESSING
### make sure that the stat is not infinite/NaN
col2 = 'MPG'
if 'AST_TO' in option:
    if data[option].isnull().values.any():
        data[option] = data[option].replace([float('inf'), -float('inf')], float('nan'))
else:
    if data[option].isnull().values.any():
        data[option] = data[option].replace([float('inf'), -float('inf')], float('nan'))
newCol = f'{option}_per_{col2}'
data[newCol] = data[option] / data[col2]
## make sure that the GP column is not infinite/NaN
if data['GP'].isnull().values.any():
    data['GP'] = data['GP'].replace([float('inf'), -float('inf')], float('nan'))
## keep only the nubmer of games played
data = data[data['GP'] >= num_gp]

## add a button to show the top players
st.write(f'{option} for the last {num_gp} games played shown below.')

### calculate percentiles for the option
data[f'Percentile'] = data[option].rank(pct=True)
top_players = sort_and_show_data(data, option, col2, team_colors, num_players) # plots the top player bar graph and scatter plot

# plot the percentile data as a bar graph with player names
# sort by percentile
data = data.sort_values(by=sort_col, ascending=False)
data.reset_index(drop=True, inplace=True)

# plot the quadrant graph with the stat vs the sort_col
plot_quadrant_scatter(data, option, sort_col, top_players, team_colors)

# keep only the top 100
data = data.head(100)
fig = px.bar(data, x='PLAYER_NAME', y='Percentile', color='Percentile', title=f'{option} Percentiles (sorted left to right by {sort_col})')
st.plotly_chart(fig, use_container_width=False)

if st.button('All Data', key='all_data_button'):
    st.write(data)
    st.button(f'Hide')

# General TODO:
# - add in the ability to select a year and then filter by that year (if possible?)
# - finally need to get advanced stats this week and work those in
# - mess w/ the color scheme, make sure it's nice