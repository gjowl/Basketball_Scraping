import streamlit as st
import os, pandas as pd

st.title('Welcome to the top stats page!')

# VARIABLES 
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
contains = 'all_game' # file you want to read

# FUNCTIONS
def sort_and_show_data(_data, _stat, n=10):
    # sort the data by the stat
    top = _data.sort_values(by=_stat, ascending=False).head(n)
    top = top.reset_index(drop=True)
    # trim to only have player name and the stat
    top = top[['PLAYER_NAME', _stat, f'{_stat}_Percentile', 'MPG']]
    if st.button(f'{_stat}', key=f'{_stat}_button'):
        st.write(top)
        st.button(f'Hide')
        # make a bar graph of percentile
        st.write(f'{_stat} Percentile')
        st.bar_chart(top[f'{_stat}_Percentile'])
        # create a simple scatter plot
        st.write(f'{_stat} vs MPG')
        st.scatter_chart(top, x=_stat, y='MPG', x_label=_stat, y_label='MPG')



# MAIN
## add in a slider
num_players = st.slider('Number of players to show:', 1, 30, 10)
## num GP to show
num_gp = st.slider('Minimum number of games played:', 1, 82, 25)
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

## SIMPLE FILTERING/DATA PREPROCESSING
## make sure that the GP column is not infinite/NaN
if data['GP'].isnull().values.any():
    data['GP'] = data['GP'].replace([float('inf'), -float('inf')], float('nan'))
## keep only the nubmer of games played
data = data[data['GP'] >= num_gp]

## PAGE SETUP BELOW
if st.button('All Data', key='all_data_button'):
    st.write(data)
    st.button(f'Hide')

## STATS TO GET TOP FOR
stats = ['PPG', 'OREB_G', 'DREB_G', 'AST_TO', 'TOV_G', 'SPG', 'BPG', 'FTA_G', '3PM_G', '2PM_G', 'NBA_FANTASY_PTS_G'] 
## TODO: get ast, rebounds, deflections, fantasy if possible

## loop through the stats
for stat in stats:
    ### make sure that the stat is not infinite/NaN
    if 'AST_TO' in stat:
        if data[stat].isnull().values.any():
            data[stat] = data[stat].replace([float('inf'), -float('inf')], float('nan'))
        ### TODO: write in a way to make APG/TO ratio for the best players  
    else:
        if data[stat].isnull().values.any():
            data[stat] = data[stat].replace([float('inf'), -float('inf')], float('nan'))
    ### calculate percentiles for the stat
    data[f'{stat}_Percentile'] = data[stat].rank(pct=True)
    print(data[f'{stat}_Percentile'])
    ### sort and show the data
    sort_and_show_data(data, stat, num_players)
    # 

