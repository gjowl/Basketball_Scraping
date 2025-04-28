import streamlit as st
import os, pandas as pd
import plotly.express as px
from functions import sort_and_show_data, plot_quadrant_scatter, create_year_data_dict

# SET PAGE CONFIG
st.set_page_config(page_title='Top Stats',
                   page_icon='🔝',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('🔝Season Stats')

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
stats = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

## TOGGLE FOR TRADITIONAL/ADVANCED STATS
st.write('**Toggle below to switch between traditional/advanced stats**')
if st.toggle('**Advanced**'):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
    stats = ['TS%', 'USG%', 'OREB%', 'DREB%', 'AST%']

year_data_dict = create_year_data_dict(datadir)
# flip the dict to get the most recent season first
year_data_dict = {k: year_data_dict[k] for k in sorted(year_data_dict.keys(), reverse=True)}
season = st.selectbox('**Season**', year_data_dict.keys(), index=None, placeholder='Season...')
if season is None:
    st.warning('*Please select a season*')
    st.stop()
data = year_data_dict[season]
max_gp = data['GP'].max()

# MAIN
## PAGE SETUP BELOW
## SELECT THE NUMBER OF PLAYERS AND GP TO FILTER 
## PICK A PLAYER TO VIEW
## SELECT THE STAT TO PLOT
## PLOTS
## TODO: fix the blurb at the top of the page

## SELECT THE NUMBER OF PLAYERS AND GP TO FILTER 
num_players = st.slider('*Number of players to show*', 1, 30, 10)
num_gp = st.slider('*Minimum number of games played*', 1, max_gp, 25)

## PICK A PLAYER TO VIEW
st.write(f'Below you can choose a stat to look at the top {num_players} ⛹🏻 who played {num_gp} games.')
st.divider()

## SELECT THE STAT TO PLOT
cols = data.columns.tolist()
stats = [col for col in stats if col in cols]
option = st.selectbox('**Stat**', stats, index=None, placeholder='Statistic...')
if option is None:
    st.warning('*Please select a stat to plot*')
    st.stop()

### FILTERING/DATA PREPROCESSING
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
st.divider()

## PLOTS
### calculate percentiles for the option
data[f'Percentile'] = data[option].rank(pct=True)
top_players = sort_and_show_data(data, option, col2, team_colors, num_players) # plots the top player bar graph and scatter plot
st.divider()

# SORT BY THE STAT SELECTED
sort_col = option_df[option_df['OPTION'] == option]['SORT'].values[0]

# plot the percentile data as a bar graph with player names
data = data.sort_values(by=sort_col, ascending=False)
data.reset_index(drop=True, inplace=True)

# plot the quadrant graph with the stat vs the sort_col
plot_quadrant_scatter(data, option, sort_col, top_players, team_colors)

# PERCENTILE BAR GRAPH (Redacted as of 2025-04-25)
## keep only the top 100
#data = data.head(100)
#fig = px.bar(data, x='PLAYER_NAME', y='Percentile', color='Percentile', title=f'{option} Percentiles (sorted left to right by {sort_col})')
#st.plotly_chart(fig, use_container_width=False)

if st.button('All Data', key='all_data_button'):
    st.write(data)
    st.button(f'Hide')