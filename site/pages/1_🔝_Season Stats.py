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
stat_options = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'FG%', 'FT%', '2P%', '3P%', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)

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
    stat_options = ['TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'W%', 'EFG%', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_RATIO', 'TM_TOV%', 'PACE', 'PIE', 'POSS', 'POSS_PG']
    advanced = True

# LOAD IN THE DATA
year_data_dict = create_year_data_dict(datadir)
# flip the dict to get the most recent season first
year_data_dict = {k: year_data_dict[k] for k in sorted(year_data_dict.keys(), reverse=True)}
season = st.selectbox('**Season**', year_data_dict.keys(), index=None, placeholder='Season...')
if season is None:
    st.warning('*Please select a season (data back to the 1996-97 season)*')
    st.stop()
data = year_data_dict[season]
max_gp = data['GP'].max()

# MAIN
## PAGE SETUP BELOW
## SELECT THE NUMBER OF PLAYERS AND GP TO FILTER 
## PICK A PLAYER TO VIEW
## SELECT THE STAT TO PLOT
## PLOTS

## SELECT THE NUMBER OF PLAYERS AND GP TO FILTER 
num_players = st.slider('***Number of players to show***', 1, 30, 10)
num_gp = st.slider('***Minimum number of games played****', 1, max_gp, 65)
st.write('**:green[65 games] played is the minimum to qualify for NBA awards as of 2023-24 season**')

## PICK A PLAYER TO VIEW
st.divider()

## SELECT THE STAT TO PLOT
cols = data.columns.tolist()
stat_options = [col for col in stat_options if col in cols]
if num_gp < 65:
    st.write(f'Choose a stat to plot the :violet[**Top {num_players}**] players who played at least :gray[**{num_gp} games**]')
else:  
    st.write(f'Choose a stat to plot the :violet[**Top {num_players}**] players who played at least :green[**{num_gp} games**]')
option = st.selectbox('**Stat**', stat_options, index=None, placeholder='Statistic...')
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
output_df = top_players.copy()
output_df = output_df[['PLAYER_NAME', option, col2, 'TEAM_ABBREVIATION']]
top_players_by_age = top_players.sort_values(by='AGE', ascending=True)
st.expander('**Top Players Data**', expanded=False)
with st.expander('**Top Players Data**', expanded=False):
    st.dataframe(output_df, use_container_width=True, hide_index=True)
st.write(f'''
        The youngest player in the :violet[**Top {num_players}**] is :rainbow[**{top_players_by_age.iloc[0]['PLAYER_NAME']}**] at **{int(top_players_by_age.iloc[0]['AGE'])}** years old, averaging :green[**{round(top_players_by_age.iloc[0][option],1)} {option}**]\n 
        The oldest player in the :violet[**Top {num_players}**] is :rainbow[**{top_players_by_age.iloc[-1]['PLAYER_NAME']}**] at **{int(top_players_by_age.iloc[-1]['AGE'])}** years old, averaging :green[**{round(top_players_by_age.iloc[-1][option],1)} {option}**]\n
         ''')
# if there are more players from the same team, write them out
# check if there are any non-unique TEAM_ABBREVIATION values in the top players
team_counts = top_players['TEAM_ABBREVIATION'].value_counts()
if len(team_counts) > 1:
    for team, count in team_counts.items():
        if count > 1:
            st.write(f':red[**{team}**] has multiple players in the :violet[**Top 10:**] :rainbow[**{", ".join(top_players[top_players["TEAM_ABBREVIATION"] == team]["PLAYER_NAME"].values)}**]')
st.divider()

# SORT BY THE STAT SELECTED
sort_col = option_df[option_df['OPTION'] == option]['SORT'].values[0]

# plot the percentile data as a bar graph with player names
data = data.sort_values(by=sort_col, ascending=False)
data.reset_index(drop=True, inplace=True)

# plot the quadrant graph with the stat vs the sort_col
plot_quadrant_scatter(data, option, sort_col, top_players, team_colors)
scatter_data = data[['PLAYER_NAME', option, sort_col, 'TEAM_ABBREVIATION']].copy()
scatter_data.sort_values(by=option, ascending=False, inplace=True)
st.expander('**Top Players Scatter Data**', expanded=False)
with st.expander('**Top Players Scatter Data**', expanded=False):
    st.write(f'''
        The :blue[**x-axis**] is the :blue[**{option}**] and the :red[**y-axis**] is the :red[**{sort_col}**], with the **{season} season** average plotted along the axes in red \n
        Most of the time, players found in the :rainbow[**top right**] quadrant performed above average, while players in the :gray[**bottom left**] quadrant performed below average. \n
         ''')
    st.dataframe(scatter_data, use_container_width=True, hide_index=True)
st.write(f'''
        The :blue[**{option}**] vs :red[**{sort_col}**] scatter plot shows the distribution of players in the league for the **{season} season**. \n
         ''')


# PERCENTILE BAR GRAPH (Redacted as of 2025-04-25)
## keep only the top 100
#data = data.head(100)
#fig = px.bar(data, x='PLAYER_NAME', y='Percentile', color='Percentile', title=f'{option} Percentiles (sorted left to right by {sort_col})')
#st.plotly_chart(fig, use_container_width=False)

if st.button('Show All Data', key='all_data_button'):
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.button(f'Hide')