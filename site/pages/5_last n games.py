import streamlit as st
import os, pandas as pd
import plotly.express as px

st.title('last n games')

# VARIABLES

# FUNCTIONS
def setup_1_game_data(_df):
    _df = _df.rename(columns={'MPG':'MIN'})
    _df.columns = [col.split('_')[0] for col in _df.columns]
    _df = _df.rename(columns={'NBA':'FTSY'})
    # get all column names that have _G in them upper or lower case
    cols = [col for col in _df.columns if '_G' in col]
    cols = [col.split('_')[0] for col in cols]
    ## MPG to MIN
    _df = _df.rename(columns={'MPG':'MIN'})
    ## split and only keep first value of name to simplify
    _df.columns = [col.split('_')[0] for col in _df.columns]
    # rename the NBA column FNTSY
    _df = _df.rename(columns={'NBA':'FTSY'})
    return _df


# MAIN
st.write('This page looks compare stats from the last 5, 10, 15, 20, 25, and 30 games played!')
st.write('You can also select either 1 or all games to see analysis on the previous game or full season statistics up to this point!')

## add in a slider for the number of games to compare
num1, num2 = st.select_slider('Number of games to analyze:',
    options=[1, 5, 10, 15, 20, 25, 30, "all"],
    value=(1,"all"))

## input directory where data is stored
dataDir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-22'

## get the data
for root, dirs, files in os.walk(dataDir):
    for file in files:
        #str1 = f'{num1}_'
        #str2 = f'{num2}_'
        if str(num1) in file:
            recent_data = pd.read_csv(os.path.join(root, file))
        if str(num2) in file:
            data2 = pd.read_csv(os.path.join(root, file))
        else:
            continue

## remove columns
recent_data = recent_data.rename(columns={'TEAM_ABBREVIATION':'TEAM'})
data2 = data2.rename(columns={'TEAM_ABBREVIATION':'TEAM'})

## subtract data for each player found in both dataframes
players = recent_data['PLAYER_NAME']
data2 = data2[data2['PLAYER_NAME'].isin(players)]
## sort by player name
recent_data = recent_data.sort_values('PLAYER_NAME')
data2 = data2.sort_values('PLAYER_NAME')
## reset the index
recent_data = recent_data.reset_index(drop=True)
data2 = data2.reset_index(drop=True)
st.write(recent_data)
st.write(data2)

## subtract two dataframes to get the difference
cols_to_keep = ['MPG','PPG','RPG','APG','SPG','BPG','TOV_PG']
diff = recent_data[cols_to_keep] - data2[cols_to_keep]
## add in the player names to the front of the dataframe
diff.insert(0, 'PLAYER_NAME', recent_data['PLAYER_NAME'])
## change none values to 0
diff = diff.fillna(0)
st.write(diff)

# add in the arrows
#diff = diff.style.applymap(lambda x: 'color: red' if x < 0 else 'color: green' if x > 0 else 'color: black')
# show in streamlit
#st.write(diff)

## graph the data
fig = px.scatter(diff, x='PPG', y='RPG', color='PLAYER_NAME', title='PPG vs RPG', labels={'x': 'PPG', 'y': 'RPG'})
st.plotly_chart(fig, use_container_width=False)


if st.button(f'{num1} games'):
    st.write(recent_data)
    st.button('Hide')
if st.button(f'{num2} games'):
    st.write(data2)
    st.button('Hide')

c1, c2 = st.columns(2)
