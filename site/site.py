import streamlit as st
import pandas as pd
import os

# prior to running: python3.8 -m venv venv
# install required programs into venv: pip install -r requirements.txt
# to run: streamlit run site.py --server.headless true
# probably add a config to the above?

# FUNCTIONS
def get_top_button(data, col, n=10):
    output_data = data.sort_values(by=col, ascending=False).head(n)
    output_data = output_data.reset_index(drop=True)
    show_button = st.button(f'Show Top {n} {col}')
    hide_button = st.button(f'Hide Top {n} {col}')
    # if button clicked once, show the top
    if show_button:
        st.write(output_data)
    if hide_button:
        st.write('')
    return

# Load data
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-12'

# get the 1 game file
datafile = os.listdir(datadir)[0]
data = pd.read_csv(os.path.join(datadir, datafile))

# SIMPLE FILTERING
# filter if players haven't played at least 80% of games (~65 game rule)
# get the max number of games played
game_count = data['GP'].max()

# filter the data
data = data[data['GP'] >= 0.8 * game_count]

# TOP 10 SCORERS
get_top_button(data, 'PPG')
## sort by ppg
#top_scorers = data.sort_values(by='PPG', ascending=False).head(10)
## reset the index
#top_scorers = top_scorers.reset_index(drop=True)
## create a button to show the top 10 scorers
#show_top_scorers = st.button('Show Top 10 Scorers')
## if the button is clicked
#if show_top_scorers:
#    # output the top 10 scorers
#    st.write(top_scorers)

# create a search button
search = st.text_input('Player Search')
search_button = st.button('Search')

# if the search button is clicked
if search_button:
    # filter the data, non-case sensitive
    player_data = data[data['PLAYER_NAME'].str.contains(search, case=False)]
    player_data = player_data.reset_index(drop=True)
    # output it to the page
    st.write(player_data)

# make a scatterplot of the 2PA_G vs 2P%
st.write('2PA_G vs 2P%')
#st.write(data[['2PA_G', '2P%']].corr())
scatter_data = data[['2PA_G', '2P%', 'PLAYER_NAME']]
# create a scatter using streamlit
st.scatter_chart(scatter_data, x='2PA_G', y='2P%', x_label='2PA_G', y_label='2P%')

# when hovering over the chart, show the player name
#st.write(data[['2PA_G', '2P%', 'PLAYER_NAME']])



# get the top 10 scorers from last night
#top_scorers = data.groupby('PLAYER_NAME')['PTS'].sum().sort_values(ascending=False).head(10)

#st.write(top_scorers)
## output it to the page
#st.write(data)

# change the website colors 