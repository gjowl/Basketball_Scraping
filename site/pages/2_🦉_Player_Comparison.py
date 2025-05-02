import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import create_year_data_dict, emoji_check, annotate_with_emojis, set_axis_text

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
stat_file = '/mnt/d/github/Basketball_Scraping/site/stats.csv'
stat_options = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'STOCKS_PG', 'FG%', 'FT%', '2P%', '3P%', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 
advanced = False
go_deeper = False
explanations = True
plot_number = 0

# READ IN THE TEAM COLORS
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)
emoji_df = pd.read_csv(emoji_file)
stat_df = pd.read_csv(stat_file)

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
            hover_template = name + f'<br>SEASON: ' + player_df['SEASON'].astype(str) + f'<br>#YEARS IN LEAGUE: ' + player_df["#YEARS IN LEAGUE"].astype(str) + '<br>' + _yaxis + ': ' + player_df[_yaxis].astype(str) + '<br>GP: ' + player_df['GP'].astype(str)
            hover_templates.append(hover_template)
    else:
        for player_df, name in zip(player_dfs, names):
            hover_template = name + f'<br>SEASON: ' + player_df['SEASON'].astype(str) + f'<br>#YEARS IN LEAGUE: ' + player_df["#YEARS IN LEAGUE"].astype(str) + '<br>' + _yaxis + ': ' + player_df[_yaxis].astype(str)
            hover_templates.append(hover_template)
    # check if colors is smaller than the number of players, if so, add more colors
    if len(colors) < len(_player_dfs):
        # add random colors to the list of colors
        for i in range(len(colors), len(_player_dfs)):
            colors.append('#' + ''.join([str(hex(mp.rand.randint(0, 255)))[2:] for _ in range(3)]))
    for player_df, hover_template, player_name, color in zip(_player_dfs, hover_templates, names, colors):
        # if the first player, create the fig
        if player_df['PLAYER_NAME'].values[0] == player_dfs[0]['PLAYER_NAME'].values[0]:
            fig = px.scatter(player_df, x=_xaxis, y=_yaxis, hover_name='PLAYER_NAME')
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='markers', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='lines', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
        else:
            # add in the hover template for the first player
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='markers', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
            fig.add_trace(go.Scatter(x=player_df[_xaxis], y=player_df[_yaxis], mode='lines', name=player_name, hovertemplate=hover_template, marker=dict(color=color, size=18, line=dict(width=2, color='DarkSlateGrey'))))
    fig.update_traces(marker=dict(size=16, line=dict(width=3, color='black')))
    fig.update_layout(title=f'{_yaxis}', xaxis_title=_xaxis, yaxis_title=_yaxis, title_font=dict(size=20))
    # keep only the lines for the legend
    for trace in fig.data:
        if trace.mode == 'lines':
            trace.showlegend = True
        else:
            trace.showlegend = False
    # update the sizes of the text
    set_axis_text(fig)
    # make the legend larger
    fig.update_layout(legend=dict(font=dict(size=16), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    st.plotly_chart(fig, key=f'compare_player_scatterplot_{n}', use_container_width=True)

# CHECKBOXES
col1, col2 = st.columns(2)
with col1:
    go_deeper = st.checkbox(':grey[**Go Deeper**]', value=False, key='go_deeper')
with col2:
    explanations = st.checkbox(':grey[**Explanations**]', value=True, key='explanations')

## TOGGLE FOR TRADITIONAL/ADVANCED STATS
if explanations:
    st.write('**Toggle to switch between :green[Traditional/Advanced] Stats**')
if st.toggle('**Advanced**'):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
    stat_options = ['TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'W%', 'EFG%', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_RATIO', 'TM_TOV%', 'PACE', 'PIE', 'POSS', 'POSS_PG']
    advanced = True
if go_deeper:
    stat_explanation = st.expander(':green[**Traditional/Advanced Stats**]', expanded=False)
    with stat_explanation:
        clicked = st.checkbox('**click me :D**', value=False, key='click_me')
        stat_types = stat_df['Type'].unique()
        for type in stat_types:
            stat_type_df = stat_df[stat_df['Type'] == type]
            st.write(f'**{type} Stats**')
            for index, row in stat_type_df.iterrows():
                stat_type = row['Type']
                if stat_type == 'Traditional':
                    st.write(f'🏀 **{row["Stat"]}** - [{row["Definition"]}]({row["Link"]})')
                else:
                    st.write(f'🏀 **{row["Stat"]}** - [{row["Definition"]}]({row["Link"]})')


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
if explanations:
    if go_deeper:
        st.write('''
                **Who was the best 3 point shooter over the course of their career? Aaron Gordon, Jerami Grant, Paul Millsap?**\n
                **Now you can select up to :green[10 players] and :green[multiple stats] to plot over time**\n
                ''')
    else:
        st.write('''
                ***Who averaged more points in their first 5 years? Lebron or Kobe? Who was more efficient?***\n
                ***Who had a better 3P% throughout their career? CP3 or Nash? Who averaged more assists?***\n
                **Pick :grey[2 players] and :grey[1 stat] to plot on a line graph over time**\n
                 ''')
st.divider()

## SELECT PLAYERS
if explanations:
    st.write('**Toggle to plot by #YEARS IN LEAGUE/SEASON**')
if st.toggle('**Compare by #YEARS IN LEAGUE**', key='compare_years', value=True):
    xaxis = '#YEARS IN LEAGUE'
else:
    xaxis = 'SEASON'

# TODO: write a way that outputs the most important takeaway from the data
player_dfs = []
if go_deeper:
    players = st.multiselect('**Select Players to Compare**', player_names_count.index.tolist(), default=['Stephen Curry', 'Steve Nash', 'Chris Paul'], key='players')
    # check if the players list is longer than 10
    if len(players) > 10:
        st.warning('*> 10 players may result in crashing, please select fewer players to compare*')
        st.stop()
    # get the data for the selected player
    for player in players:
        player_df = player_names[player_names['PLAYER_NAME'] == player].reset_index(drop=True)
        player_df['#YEARS IN LEAGUE'] = player_df['SEASON'].astype(int) - player_df['SEASON'].astype(int).min()
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
        remove_cols = ['PLAYER_NAME', 'SEASON', 'YEAR', 'MPG', '#YEARS IN LEAGUE', 'FGM', 'FGA', 'FGM_PG', 'FGA_PG', 'FG%', 'AST_TO']
        cols = [col for col in cols if col not in remove_cols]
        stats = st.multiselect('**Select Stats to Compare**', cols[6:], default=['TS%', 'USG%', 'AST%'], key='stats')
else:
    player_1 = st.selectbox('**Player 1**', player_names_count.index.tolist(), index=0, key='player_1')
    player_names_2 = player_names_count[player_names_count.index != player_1].index.tolist()
    player_2 = st.selectbox('**Player 2**', player_names_2, index=1, key='player_2')
    players = [player_1, player_2]
    for player in players:
        player_df = player_names[player_names['PLAYER_NAME'] == player].reset_index(drop=True)
        player_df['#YEARS IN LEAGUE'] = player_df['SEASON'].astype(int) - player_df['SEASON'].astype(int).min()
        player_dfs.append(player_df)
    stat1 = st.selectbox('**Select Stat**', stat_options, index=0, key='stat')
    stats = [stat1]

## TOGGLE TO PLOT BY YEARS IN LEAGUE OR SEASON

cols = ['PLAYER_NAME', 'SEASON', '#YEARS IN LEAGUE', 'GP']
for stat in stats:
    cols.append(stat)
st.divider()

# keep the first 3 columns and the stat columns
final_dfs, avgs = [], {} 
output_df = pd.DataFrame()
for player_df in player_dfs:
    player_df = player_df[cols]
    final_dfs.append(player_df)
    player = player_df['PLAYER_NAME'].values[0]
    for stat in stats:
        # get the average of the stat for the player
        avg = player_df[stat].mean().round(2)
        avgs[player] = {}
        avgs[player][stat] = avg

# PLOTS
if go_deeper:
    for stat in stats:
        compare_player_scatterplot(final_dfs, xaxis, stat, plot_number)
        plot_number+=1
else:
    compare_player_scatterplot(final_dfs, xaxis, stat1, plot_number)
    plot_number+=1
    for player, value in avgs.items():
        st.write(f'**{player}** - {stat1}: {value[stat1]}')

st.divider()

# add a button to show the player data
st.expander('**Show Player Data**', expanded=False)
with st.expander('**Show player data**', expanded=False):
    columns = st.columns(len(final_dfs))
    for player_df, name, col in zip(final_dfs, players, columns):
        player_df = player_df.drop(columns=['PLAYER_NAME'])
        with col:
            st.write(f'**{name}**')
            st.dataframe(player_df, use_container_width=True, hide_index=True)

# PRINT OUT EMOJI PLAYERS
sum = len(players) + len(stats)
if go_deeper and sum >= 7 and explanations == False:
    emoji_players = emoji_df[emoji_df['PLAYER_NAME'].isin(players)]
    if len(emoji_players) > 0:
        st.expander(f'**Emojis**', expanded=True)
        with st.expander(f':rainbow[Emojis]', expanded=False):
            player_emoji_list = []
            for player in emoji_players['PLAYER_NAME'].tolist():
                player_emoji = annotate_with_emojis(player, emoji_df)
                player_emoji_list.append(player_emoji)
            st.write(f"{' | '.join(player_emoji_list)}")

## Some fun player comparison examples that you NEED to be able to do for this website to work out:
## - Nash vs Steph
## - MKG vs Haywood Highsmith
## - Matas vs Tatum (from his first year with the type of game he has (percentages and usage and advanced might agree?); let's see if he adds the mid-range and passing next!)
## - Daniel Gafford vs Gary Payton II