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
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
contains = 'all_game' # file you want to read

# FUNCTIONS
#def make_spec(_xCol, _yCol, _labelCol):
#    # check if col name has a _ in it
#    if '_' in _xCol:
#        xColName = _xCol.split('_')[0]
#    elif 'PG' in _xCol:
#        xColName = _xCol[:-2]
#    if '_' in _yCol:
#        yColName = _yCol.split('_')[0]
#    elif 'PG' in _yCol:
#        yColName = _yCol[:-2]
#    spec = {
#        'mark': {'type': 'circle', 'tooltip': True},
#        'params': [
#            {'name': 'interval_selection', 'select': 'interval'},
#            {'name': 'point_selection', 'select': 'point'}
#        ],
#        # change the axis labels
#        'encoding': {
#            'x': {'field': _xCol, 'type': 'quantitative'},
#            'y': {
#                'field': _yCol, 'type': 'quantitative', 'scale': {'zero': False}, 'title': yColName, 'axis': {'labelOverlap': 'parity'}, 'labelAngle': 90
#                },
#            'color': {'field': _labelCol, 'type': 'nominal'},
#            'fillOpacity': {
#                'condition': {
#                    'param': 'point_selection', 'value': 1},
#                    'value': 0.3,
#                },
#            'legend': {'title': 'Player Name'},
#            'layout': {'columns': 2},
#            'config': {'axisY': {'minExtent': 40, 'labelAngle': 100}, 'view': {'stroke': 'transparent'}},
#            },
#    }
#    return spec

def concat_col_names(_data, _col1, _col2):
#    # check if col name has a _ in it
#    if '_' in _xCol:
#        xColName = _xCol.split('_')[0]
#    elif 'PG' in _xCol:
#        xColName = _xCol[:-2]
#    if '_' in _yCol:
#        yColName = _yCol.split('_')[0]
#    elif 'PG' in _yCol:
#        yColName = _yCol[:-2]
    _data['newCol'] = _data[_col1] / _data[_col2]
    return

# sort and show the data
def sort_and_show_data(_data, _col1, _col2, n=10):
    # sort the data by the stat
    top = _data.sort_values(by=_col1, ascending=False).head(n)
    top = top.reset_index(drop=True)
    # trim to only have player name and the stat
    top = top[['PLAYER_NAME', _col1, f'{_col1}_Percentile', _col2]]
    #top = top[['PLAYER_NAME', _col1, _col2]]
    newCol = f'{_col1}_per_{_col2}'
    top[newCol] = top[_col1] / top[_col2]
    if st.button(f'{_col1}', key=f'{_col1}_button'):
        st.write(top)
        # make a bar graph of percentile
        st.write(f'{_col1} Percentile')
        # make spec for vega-lite charts
        fig1 = px.scatter(top, x=_col2, y=_col1, color='PLAYER_NAME', title=f'{_col1} vs {_col2}', labels={'x': _col2, 'y': _col1})
        fig2 = px.scatter(top, x=_col1, y=newCol, color='PLAYER_NAME', title=f'{_col1} vs {newCol}', labels={'x': _col1, 'y': newCol})
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig1, use_container_width=False)
        with c2:
            st.plotly_chart(fig2, use_container_width=False)
        #spec1 = make_spec(_col2, _col1, 'PLAYER_NAME') # scatter of stat2 vs stat1
        #spec2 = make_spec(_col1, newCol, 'PLAYER_NAME') # scatter of stat1 vs (stat1 per stat2); ex. point per minute, oreb per minute, etc.
        ## make a scatter plot of the stat vs MPG
        #st.vega_lite_chart(top, spec1)
        #st.vega_lite_chart(top, spec2)
        ##st.write(f'{_col1} vs MPG')
        ##st.scatter_chart(top, x=_col1, y=_col2, x_label=_col1, y_label=_col2)
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
if st.button('All Data', key='all_data_button'):
    st.write(data)
    st.button(f'Hide')

## STATS TO GET TOP FOR
stats = ['PPG', 'OREB_G', 'DREB_G', 'AST_TO', 'TOV_G', 'SPG', 'BPG', 'FTA_G', '3PM_G', '3PA_G', '2PM_G', '2PA_G', 'NBA_FANTASY_PTS_G'] 
## TODO: get ast, rebounds, deflections, fantasy if possible

## loop through the stats
col2 = 'MPG'
for stat in stats:
    ### make sure that the stat is not infinite/NaN
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
    sort_and_show_data(data, stat, col2, num_players)
    # 

