import streamlit as st
import os, pandas as pd
import plotly.express as px


# SET PAGE CONFIG
st.set_page_config(page_title='Top Stats',
                   page_icon='',
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

# FUNCTIONS

# concats the column names, removing the _G and PG 
def concat_col_names(_xCol, _yCol):
    # check if col name has a _ in it
    if '_' in _yCol:
        yColName = _yCol.split('_')[0]
    elif 'PG' in _yCol:
        yColName = _yCol[:-2]
    if '_' in _xCol:
        xColName = _xCol.split('_')[0]
        colName = f'{xColName}_{yColName}'
    elif 'PG' in _xCol:
        xColName = _xCol[:-1]
        colName = f'{xColName}{yColName}'
    return colName

# sort and show the data
def sort_and_show_data(_data, _col1, _col2, _button, n=10):
    # sort the data by the stat
    top = _data.sort_values(by=_col1, ascending=False).head(n)
    top = top.reset_index(drop=True)
    # trim to only have player name and the stat
    percentile_col = f'{_col1}_Percentile'
    top = top[['PLAYER_NAME', _col1, _col2, percentile_col]]
    #top = top[['PLAYER_NAME', _col1, _col2]]
    newCol = concat_col_names(_col1, _col2)
    top[newCol] = top[_col1] / top[_col2]
    # normalize the data
    with _button:
        #st.button(f'{_col1}', key=f'{_col}_button')
        if st.button(f'{_col1}', key=f'{_col1}_button'):
            st.write(top)
            # make spec for vega-lite charts
            fig1 = px.scatter(top, x=_col2, y=_col1, color='PLAYER_NAME', title=f'{_col2} vs {_col1}', labels={'x': _col2, 'y': _col1}, size=f'{percentile_col}')
            c1 = st.columns(1)
            with c1:
                st.plotly_chart(fig1, use_container_width=False)
            st.button(f'Hide')


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
## STATS TO GET TOP FOR
stats = ['PPG', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'SPG', 'BPG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1,1])
cols = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13]
## TODO: get ast, rebounds, deflections, fantasy if possible
## TODO: add up attempts for 2PM and 3PM AND FTA/2 to get total attempts; maybe pair this stat with usage in some way?

## loop through the stats
col2 = 'MPG'
for col, stat in zip(cols, stats):
    #with col:
    #    st.button(f'{stat}', key=f'{stat}_button')
    #    ### make sure that the stat is not infinite/NaN
    if 'AST_TO' in stat:
        if data[stat].isnull().values.any():
            data[stat] = data[stat].replace([float('inf'), -float('inf')], float('nan'))
        ### TODO: write in a way to make APG/TO ratio for the best players  
    else:
        if data[stat].isnull().values.any():
            data[stat] = data[stat].replace([float('inf'), -float('inf')], float('nan'))
    newCol = f'{stat}_per_{col2}'
    data[newCol] = data[stat] / data[col2]
    ### calculate percentiles for the stat
    data[f'{stat}_Percentile'] = data[newCol].rank(pct=True)
    ### sort and show the data
    sort_and_show_data(data, stat, col2, col, num_players)
    # 

if st.button('All Data', key='all_data_button'):
    st.write(data)
    st.button(f'Hide')
