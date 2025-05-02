import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import create_year_data_dict, emoji_check, annotate_with_emojis

# SET PAGE CONFIG
st.set_page_config(page_title='Season Trajectories',
                   page_icon='📈',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('📈 Season Trajectories')

# VARIABLES 
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
#datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD'
colors = '/mnt/d/github/Basketball_Scraping/site/team_colors_hex.csv'
options = '/mnt/d/github/Basketball_Scraping/site/options.csv'
emoji_file = '/mnt/d/github/Basketball_Scraping/site/emoji_players.csv'

# HARDCODED STAT GROUPS
threes = ['3PM_PG', '3PA_PG', '3P%']
twos = ['2PM_PG', '2PA_PG', '2P%']
fgs = ['FGM_PG', 'FGA_PG', 'FG%']
fts = ['FTM_PG', 'FTA_PG', 'FT%']
general = ['APG', 'RPG', 'DREB_PG', 'OREB_PG', 'TOV_PG', 'SPG', 'BPG', 'PF_PG']
stat_options = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'FG%', 'FT%', '2P%', '3P%', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 
advanced = False

# READ IN THE TEAM COLORS
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)
emoji_df = pd.read_csv(emoji_file)

# MAIN
# TODO: might it be interesting to only look at specific teams?
# TODO: figure out what might be interesting here, or may have to bail on it for now
# TODO: st.multiselect, st.pills may be a good tool to use for the comparing stats
## PAGE SETUP BELOW
## TOGGLE FOR TRADITIONAL/ADVANCED STATS
## SELECT THE NUMBER OF YEARS
## SELECT THE NUMBER OF GAMES PLAYED
## SELECT THE MAXIMUM NUMBER OF PLAYERS TO PLOT
## SELECT THE STAT TO PLOT
## PLOTS
# st.progress, st.spinner, st.status might be good tools for loading times

# if you were to make this kind of like an interactive walkthrough; populating the page for each person being added would be helpful
# I think making this an interactive page is for the best!
# Let people pick the stat they want to see against year
# make it so that you can make up to 3 (?) simultaneously

## TOGGLE FOR TRADITIONAL/ADVANCED STATS
st.write('**Toggle to switch between :green[Traditional/Advanced] Stats**')
stat_explanation = st.expander(':green[**Traditional/Advanced Stats**]', expanded=False)
with stat_explanation:
        st.write('''
                :green[**Traditional**]\n
                🏀 **PPG** - Points Per Game\n
                🏀 **APG** - Assists Per Game\n
                🏀 **RPG** - Rebounds Per Game\n
                🏀 **SPG** - Steals Per Game\n
                🏀 **BPG** - Blocks Per Game\n
                🏀 **OREB_PG** - Offensive Rebounds Per Game\n
                🏀 **DREB_PG** - Defensive Rebounds Per Game\n
                🏀 **AST_TO** - Assist to Turnover Ratio\n
                🏀 **TOV_PG** - Turnovers Per Game\n
                🏀 **FTA_PG** - Free Throws Attempted Per Game\n
                🏀 **3PM_PG** - 3 Point Field Goals Made Per Game\n
                🏀 **3PA_PG** - 3 Point Field Goals Attempted Per Game\n
                🏀 **2PM_PG** - 2 Point Field Goals Made Per Game\n
                🏀 **2PA_PG** - 2 Point Field Goals Attempted Per Game\n
                🏀 **NBA_FANTASY_PTS_PG** - NBA Fantasy Points Per Game\n
                :green[**Advanced**]\n
                🏀 **TS%** - True Shooting Percentage\n
                🏀 **USG%** - Usage Percentage\n
                🏀 **OREB%** - Offensive Rebound Percentage\n
                🏀 **DREB%** - Defensive Rebound Percentage\n
                🏀 **AST%** - Assist Percentage\n
                🏀 **W%** - Winning %\n
                🏀 **EFG%** - Effective Field Goal Percentage\n
                🏀 **OFF_RATING** - Offensive Rating\n
                🏀 **DEF_RATING** - Defensive Rating\n
                🏀 **NET_RATING** - Net Rating\n
                🏀 **AST_RATIO** - Assist Ratio\n
                🏀 **TM_TOV%** - Team Turnover Percentage\n
                🏀 **PACE** - Pace\n
                🏀 **PIE** - Player Impact Estimate\n
                🏀 **POSS** - Possessions\n
                🏀 **POSS_PG** - Possessions Per Game\n
                ''')

if st.toggle('**Advanced**'):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
    advanced = True

## traverse directory to load data
year_data_dict = create_year_data_dict(datadir)

## get all the unique player names from the year_data_dict
data_df = pd.DataFrame()
for key in year_data_dict.keys():
    # add the year column to the dataframe
    year_df = year_data_dict[key]
    year_df['YEAR'] = key
    data_df = pd.concat([data_df, year_df], ignore_index=True)
    
## check if the player name is duplicated, if so remove the duplicates
#data_df_no_dups = data_df['PLAYER_NAME'].drop_duplicates(keep=False)
#
## if the player is in the list, remove them from the dataframe
#data_df = data_df[~data_df['PLAYER_NAME'].isin(data_df_no_dups)]
#data_df = data_df.reset_index(drop=True)
# count the number of instances of the player names in the dataframe
data_df_count = data_df['PLAYER_NAME'].value_counts()

## SELECT THE NUMBER OF YEARS
# add an input slider for the number of years to filter by
count = st.slider('**Select the minimum # of years played in the league**', 1, 10, 5) 
data_df_count = data_df_count[data_df_count >= count]
data_df = data_df[data_df['PLAYER_NAME'].isin(data_df_count.index)]

## SELECT THE NUMBER OF GAMES PLAYED
# TODO: might be interesting to do some kind of density plot of GP
games_played = st.slider('**Select the # of games played to filter by**', 1, 82, 65) # 82 is the max number of games played in a season
data_df = data_df[data_df['GP'] > games_played]

## SELECT THE MAXIMUM NUMBER OF PLAYERS TO PLOT
# TODO: might not need this?
num_players = st.slider('**Select the maximum # of players to plot per season**', 1, 25, 5)
color = ':green'
if games_played < 65:
    gp_color = ':gray'
else:
    gp_color = ':green'
# Dynamic blurb    
st.write(f'''
        **Searching for the :violet[**Top {num_players}**] players who played for :green[**>= {count}**] seasons and played {gp_color}[**>= {games_played}**] games in the season** 
         ''')
st.divider()


## CHOOSE THE STAT TO PLOT
# make a search bar for the stats to plot
#stat_options = data_df.columns[3:] # from the GP column and on
start_index = stat_options.index('3PM_PG')
if advanced:
    stat_options = ['TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'W%', 'EFG%', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_RATIO', 'TM_TOV%', 'PACE', 'PIE', 'POSS', 'POSS_PG']
    start_index = stat_options.index('USG%')

stat = st.selectbox('**Select the stat to plot**', stat_options, index=start_index) # from the GP column and on

stat_2 = 'MPG'
if stat == 'MPG':
    stat_2 = 'GP'
# TODO: add a short wait here (checking stat type...) (make it feel like an old school kind of vibe (that can be toggled))
if stat in threes:
    stat_2 = '3PA_PG'
    attempts = st.slider('**Select the minimum number of 3PA_PG to filter by**', 1, 10, 3) 
    data_df = data_df[data_df[stat_2] >= attempts]
if stat in twos:
    stat_2 = '2PA_PG'
    attempts = st.slider('**Select the minimum number of 2PA_PG to filter by**', 1, 10, 5) 
    data_df = data_df[data_df[stat_2] >= attempts]
if stat in general:
    max_stat = int(data_df[stat].max())
    attempts = st.slider(f'**Select the minimum number of **{stat}** to filter by**', 1, max_stat, 2)
    data_df = data_df[data_df[stat] >= attempts]
# keep only the players with the top 100 of the stat for each year
data_df = data_df.sort_values(by=stat, ascending=False).groupby('SEASON').head(num_players)
# sort the players by year
data_df = data_df.sort_values(by='SEASON')
fig = px.scatter(data_df, x='SEASON', y=stat, color='PLAYER_NAME', hover_name='PLAYER_NAME', title=f'{stat} vs SEASON')
# separate the points out of a straight line
fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
st.divider()

# 
label = '**Toggle to show trajectories for players who appear on the graph in multiple seasons**'
st.write('**Toggle to show trajectories for players who appear on the graph in multiple seasons**')
# PLAYER TRAJECTORY TOGGLE
if st.toggle('**Show Player Trajectories**', key='show_lines', value=False):
    fig.update_traces(mode='markers+lines')
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.expander('**Top Players Data**', expanded=False)
with st.expander(':green[**Top Players Data**]', expanded=False):
    if st.toggle('**Show Condensed Data**', key='show_data', value=True):
        data_df = data_df[['PLAYER_NAME', 'SEASON', 'GP', stat, stat_2, 'TEAM_ABBREVIATION']]
        data_df = data_df.sort_values(by=['SEASON', stat], ascending=False)
        st.dataframe(data_df, use_container_width=True, hide_index=True)
    else:
        data_df = data_df.sort_values(by=['SEASON', stat], ascending=False)
        st.dataframe(data_df, use_container_width=True, hide_index=True)
st.divider()

# WRITE THE EMOJIS
st.expander('**Emojis**', expanded=False)
with st.expander(':green[**Emojis**]', expanded=False):
    emoji_players = emoji_check(emoji_df, data_df)
    # write out the players with emojis
    player_emoji_list = []
    for player in emoji_players['PLAYER_NAME']:
        player_emoji = annotate_with_emojis(player, emoji_df)
        player_emoji_list.append(player_emoji)
    st.write(f"{' | '.join(player_emoji_list)}")
    st.write(f'''
    "おめでとうございます,絵文字を見つけました/O-me-de-tou-go-za-i-mas,E-mo-ji o mi-tsu-ke-ma-shi-ta" - "Congrats, you found some emojis :D"\n
    ''')

## TODO: these might actually just be better as yearly boxplots; maybe add a button to toggle between the two?
# another idea: get the biggest movers from year to year to identify players that were starting to space out the league at the 4 and 5 positions