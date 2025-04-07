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
colors = '/mnt/d/github/Basketball_Scraping/site/team_colors_hex.csv'
options = '/mnt/d/github/Basketball_Scraping/site/options.csv'

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

# FUNCTIONS
# changes the figure to the team colors
def change_to_team_colors(_fig, _data, team_colors):
    # set the color for each player to be the same as their team color
    for i in range(len(_data)):
        # get the team abbreviation and match it to the hexcolors file
        team = _data['TEAM_ABBREVIATION'][i]
        # get the color from the team_colors file
        color = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
        _fig.data[i].marker.color = color

# sort and show the data
def sort_and_show_data(_data, _col1, _col2, n=10):
    # sort the data by the stat
    top = _data.sort_values(by=_col1, ascending=False).head(n)
    top = top.reset_index(drop=True)
    # trim to only have player name and the stat
    percentile_col = f'Percentile'
    # show the data in a bar graph with player names and the stat above the bar
    fig = px.bar(top, x='PLAYER_NAME', y=_col1, color='PLAYER_NAME', title=f'Top {n} Players - {_col1}', labels={'x': 'Player Name', 'y': _col1})
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    # fit the figure to the screen
    fig.update_layout(yaxis=dict(range=[0, top[_col1].max() * 1.1]), xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    # remove the legend
    fig.update_layout(showlegend=False)
    # make spec for vega-lite charts
    fig1 = px.scatter(top, x=_col2, y=_col1, color='PLAYER_NAME', title=f'{_col2} vs {_col1}', labels={'x': _col2, 'y': _col1}, size=f'{percentile_col}')
    change_to_team_colors(fig1, top, team_colors)
    change_to_team_colors(fig, top, team_colors)
    #fig2 = px.scatter(top, x=_col1, y=newCol, color='PLAYER_NAME', title=f'{_col1} vs {newCol}', labels={'x': _col1, 'y': newCol}, size=f'{percentile_col}')
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.plotly_chart(fig1, use_container_width=False)
    st.button(f'Hide')
    return top

# plot the scatter plot of the stat vs the sort column
def plot_quadrant_scatter(_data, _col1, _col2, _top):
    # calculate the average of the stat
    avg = _data[_col1].mean()
    # get the difference from the average
    avg_sort = _data[_col2].mean()
    # plot the data
    fig2 = px.scatter(_data, x=_col1, y=_col2, color='PLAYER_NAME', title=f'{_col1} vs {_col2}')
    # add a line at 0 for both axes
    fig2.add_hline(y=avg_sort, line_color='red', line_width=1, line_dash='dash')
    fig2.add_vline(x=avg, line_color='red', line_width=1, line_dash='dash')
    fig2.update_traces(marker=dict(size=10))
    # remove the legend
    fig2.update_layout(showlegend=False)
    # set all points to gray
    fig2.update_traces(marker=dict(color='gray', line=dict(width=1, color='black')))
    # highlight the top players in the scatter plot
    for i in range(len(_top)):
        # get the player name and team abbreviation
        player = _top['PLAYER_NAME'][i]
        print(player)
        team = _top['TEAM_ABBREVIATION'][i]
        # color the player name and team abbreviation
        color = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
        # find the player in the data and set the color to the team color
        player_index = _data[_data['PLAYER_NAME'] == player].index[0]
        print(player_index)
        fig2.data[player_index].marker.color = color
    st.plotly_chart(fig2, use_container_width=False)

# MAIN
## PAGE SETUP BELOW
## TODO: add in the setup of the page details here







## add in sliders for the number of players and games played
num_players = st.slider('Number of players to show:', 1, 30, 10)
num_gp = st.slider('Minimum number of games played:', 1, 82, 25)

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

## STATS TO GET
stats = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 
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

## TODO: add up attempts for 2PM and 3PM AND FTA/2 to get total attempts; maybe pair this stat with usage in some way?

## add a button to show the top players
st.write(f'{option} for the last {num_gp} games played shown below.')

### calculate percentiles for the option
data[f'Percentile'] = data[option].rank(pct=True)
top_players = sort_and_show_data(data, option, col2, num_players) # plots the top player bar graph and scatter plot

# plot the percentile data as a bar graph with player names
# sort by percentile
data = data.sort_values(by=sort_col, ascending=False)
data.reset_index(drop=True, inplace=True)

# plot the quadrant graph with the stat vs the sort_col
plot_quadrant_scatter(data, option, sort_col, top_players)

# keep only the top 100
data = data.head(100)
fig = px.bar(data, x='PLAYER_NAME', y='Percentile', color='Percentile', title=f'{option} Percentiles (sorted left to right by {sort_col})')
st.plotly_chart(fig, use_container_width=False)

if st.button('All Data', key='all_data_button'):
    st.write(data)
    st.button(f'Hide')