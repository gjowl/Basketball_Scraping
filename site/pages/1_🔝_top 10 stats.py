import streamlit as st
import os, pandas as pd

st.title('Welcome to the top stats page!')

# VARIABLES 
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-12'
contains = '1_game' # file you want to read
# TODO: get all games played as the file for this

# add in a slider
num_players = st.slider('Number of players to show:', 1, 30, 10)
st.write(f'Here, you can view the top {num_players} players in various statistical categories.')
#num_players = 10 # number of players to show

# traverse directory to load data
for root, dirs, files in os.walk(datadir):
    for file in files:
        # look if the name of the file is what you want
        if contains in file:
            datafile = os.path.join(root, file)
            data = pd.read_csv(datafile)

# remove the GP column
data = data.drop(columns='GP')

# simple filtering/data preprocessing

# PAGE SETUP BELOW
if st.button('All Data', key='all_data_button'):
    st.write(data)
    st.button(f'Hide')

# STATS TO GET TOP FOR
stats = ['PPG', 'AST_TO', 'SPG', 'BPG', 'FTA_G', '3PM_G', '2PM_G'] 
# TODO: get ast, rebounds, deflections, fantasy if possible

# loop through the stats
for stat in stats:
    # make sure that the stat is not infinite/NaN
    if 'AST_TO' in stat:
        if data[stat].isnull().values.any():
            data[stat] = data[stat].replace([float('inf'), -float('inf')], float('nan'))
        # TODO: write in a way to make APG/TO ratio for the best players  
    else:
        if data[stat].isnull().values.any():
            data[stat] = data[stat].replace([float('inf'), -float('inf')], float('nan'))

    # sort the data by the stat
    top = data.sort_values(by=stat, ascending=False).head(num_players)
    top = top.reset_index(drop=True)
    # trim to only have player name and the stat
    top = top[['PLAYER_NAME', stat]]
    if st.button(f'Top 10 {stat}', key=f'{stat}_button'):
        #if "button_clicked" not in st.session_state:
        #    st.session_state["button_clicked"] = False
        st.write(top)
        st.button(f'Hide')