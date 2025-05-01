import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import create_year_data_dict, emoji_check, annotate_with_emojis

# SET PAGE CONFIG
st.set_page_config(page_title='Player Comparison',
                   page_icon='🦉',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('🦉 Player Comparison')

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
emoji_file = '/mnt/d/github/Basketball_Scraping/site/emoji_players.csv'
stat_options = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'FG%', 'FT%', '2P%', '3P%', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 
advanced = False
plot_number = 0

# READ IN THE TEAM COLORS
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)
emoji_df = pd.read_csv(emoji_file)

# FUNCTIONS
# TODO: fix the colors here for up to 10 players
colors = ['#F27522', 'lightgrey', '#4082de', '#ADD8E6', '#F08080', '#FFA07A', '#FFE4B5', '#FF4500', '#FFD700', '#00FF00']
def compare_player_scatterplot(_player_dfs, _xaxis, _yaxis, n=0):
    names, hover_templates = [], []
    for player_df in _player_dfs:
        names.append(player_df['PLAYER_NAME'].values[0])
    # make the hover template for the player name
    if _yaxis != 'GP':
        for player_df, name in zip(player_dfs, names):
            hover_template = name + f'<br>{_xaxis}: ' + player_df[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + player_df[_yaxis].astype(str) + '<br>GP: ' + player_df['GP'].astype(str)
            hover_templates.append(hover_template)
    else:
        for player_df, name in zip(player_dfs, names):
            hover_template = name + f'<br>{_xaxis}: ' + player_df[_xaxis].astype(str) + '<br>' + _yaxis + ': ' + player_df[_yaxis].astype(str)
            hover_templates.append(hover_template)
    # check if colors is smaller than the number of players, if so, add more colors
    if len(colors) < len(_player_dfs):
        # add random colors to the list of colors
        for i in range(len(colors), len(_player_dfs)):
            colors.append('#' + ''.join([str(hex(mp.rand.randint(0, 255)))[2:] for _ in range(3)]))
    for player_df, hover_template, player_name, color in zip(_player_dfs, hover_templates, names, colors):
        # if the first player, create the fig
        if player_df['PLAYER_NAME'].values[0] == player_dfs[0]['PLAYER_NAME'].values[0]:
            fig = px.scatter(player_df, x=_xaxis, y=_yaxis, color='PLAYER_NAME', hover_name='PLAYER_NAME')
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='markers', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='lines', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
        else:
            # add in the hover template for the first player
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='markers', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='lines', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
    # remove the legend
    fig.update_traces(marker=dict(size=16, line=dict(width=3, color='black')))
    fig.update_layout(showlegend=False)
    fig.update_layout(title=f'{_yaxis} per {_xaxis}', xaxis_title=_xaxis, yaxis_title=_yaxis)
    st.plotly_chart(fig, key=f'compare_player_scatterplot_{n}', use_container_width=True)

## TOGGLE FOR TRADITIONAL/ADVANCED STATS
st.write('**Toggle to switch between :green[Traditional/Advanced] Stats**')
# TODO: show button for what the traditional/advanced stats are
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
                🏀 **OFF_RATING** - Offensive Rating\n
                🏀 **DEF_RATING** - Defensive Rating\n
                🏀 **NET_RATING** - Net Rating\n
                🏀 **AST%** - Assist Percentage\n
                🏀 **AST_RATIO** - Assist Ratio\n
                🏀 **TM_TOV%** - Team Turnover Percentage\n
                🏀 **PACE** - Pace\n
                🏀 **PIE** - Player Impact Estimate\n
                🏀 **POSS** - Possessions\n
                🏀 **EFG%** - Effective Field Goal Percentage\n
                ''')
if st.toggle('**Advanced**'):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
    stat_options = ['TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'W%', 'EFG%', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_RATIO', 'TM_TOV%', 'PACE', 'PIE', 'POSS', 'POSS_PG']
    advanced = True

# INITIAL DATA PROCESSING
year_data_dict = create_year_data_dict(datadir)

## GET ALL THE UNIQUE PLAYER NAMES FROM THE YEAR_DATA_DICT
player_names = pd.DataFrame()
for key in year_data_dict.keys():
    # add the year column to the dataframe
    year_df = year_data_dict[key]
    year_df['YEAR'] = key
    player_names = pd.concat([player_names, year_df], ignore_index=True)
    
# check if the player name is duplicated, if so remove the duplicates
player_names_no_dups = player_names['PLAYER_NAME'].drop_duplicates(keep=False)
# if the player is in the list, remove them from the dataframe
player_names = player_names[~player_names['PLAYER_NAME'].isin(player_names_no_dups)]
# reset the index of the dataframe
player_names = player_names.reset_index(drop=True)
# count the number of instances of the player names in the dataframe
player_names_count = player_names['PLAYER_NAME'].value_counts()

# MAIN
## PAGE SETUP BELOW
## PAGE BLURB
## TOGGLE FOR TRADITIONAL/ADVANCED STATS
## SELECT PLAYERS
## TOGGLE TO PLOT BY YEARS IN LEAGUE OR SEASON
## SELECT STATS TO PLOT
## PLOTS

## PAGE BLURB
# TODO: add a bit more a blurb here for the page
st.write('**This page allows you to compare the stats of players over the years they have played in the league since the 1996-97 season (as far back as nba.com has data).**')
st.divider()

## SELECT PLAYERS
# TODO: write a way that outputs the most important takeaway from the data
players = st.multiselect('**Select Players to Compare**', player_names_count.index.tolist(), default=['Stephen Curry', 'Steve Nash', 'Chris Paul'], key='players')
# check if the players list is longer than 10
if len(players) > 10:
    st.warning('*> 10 players may result in crashing, please select fewer players to compare*')
    st.stop()
# get the data for the selected player
player_dfs = []
for player in players:
    player_df = player_names[player_names['PLAYER_NAME'] == player].reset_index(drop=True)
    player_df['#YEARS_IN_LEAGUE'] = player_df['SEASON'].astype(int) - player_df['SEASON'].astype(int).min()
    player_dfs.append(player_df)

## SELECT STATS TO PLOT 
cols = player_dfs[0].columns.tolist()
stat_options = [col for col in stat_options if col in cols]
if advanced == False:
    stats = st.multiselect('**Select Stats to Compare**', stat_options, default=['PPG', '3P%', 'FG%'], key='stats')
else:
    cols = player_dfs[0].columns.tolist()
    # remove columns that have _RANK in them
    cols = [col for col in cols if '_RANK' not in col]
    remove_cols = ['PLAYER_NAME', 'SEASON', 'YEAR', 'MPG', '#YEARS_IN_LEAGUE', 'FGM', 'FGA', 'FGM_PG', 'FGA_PG', 'FG%', 'AST_TO']
    cols = [col for col in cols if col not in remove_cols]
    stats = st.multiselect('**Select Stats to Compare**', cols[6:], default=['TS%', 'USG%', 'AST%'], key='stats')

## TOGGLE TO PLOT BY YEARS IN LEAGUE OR SEASON
if st.toggle('**Compare by #YEARS_IN_LEAGUE**', key='compare_years', value=True):
    xaxis = '#YEARS_IN_LEAGUE'
else:
    xaxis = 'SEASON'
cols = ['PLAYER_NAME', xaxis, 'GP']
for stat in stats:
    cols.append(stat)


st.divider()



# keep the first 3 columns and the stat columns
final_dfs = []
for player_df in player_dfs:
    player_df = player_df[cols]
    final_dfs.append(player_df)

# PLOTS
for stat in stats:
    compare_player_scatterplot(final_dfs, xaxis, stat, plot_number)
    plot_number+=1
st.divider()

# PRINT OUT EMOJI PLAYERS
emoji_players = emoji_df[emoji_df['PLAYER_NAME'].isin(players)]
if len(emoji_players) > 0:
    st.expander(f'**Emojis**', expanded=True)
    with st.expander(f':green[Emojis]', expanded=False):
        player_emoji_list = []
        for player in emoji_players['PLAYER_NAME'].tolist():
            player_emoji = annotate_with_emojis(player, emoji_df)
            player_emoji_list.append(player_emoji)
        st.write(f"{' | '.join(player_emoji_list)}")

# add a button to show the player data
if st.button('Show player data', key='show_player_data'):
    columns = st.columns(len(final_dfs))
    for player_df, name, col in zip(final_dfs, players, columns):
        player_df = player_df.drop(columns=['PLAYER_NAME'])
        with col:
            st.write(f'**{name}**')
            st.dataframe(player_df, use_container_width=True, hide_index=True)
    st.button('Hide player data', key='hide_player_data')

## Some fun player comparison examples that you NEED to be able to do for this website to work out:
## - Nash vs Steph
## - MKG vs Haywood Highsmith
## - Matas vs Tatum (from his first year with the type of game he has (percentages and usage and advanced might agree?); let's see if he adds the mid-range and passing next!)
## - Daniel Gafford vs Gary Payton II