import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import create_year_data_dict, emoji_check, annotate_with_emojis, set_axis_text
import random

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
examples = '/mnt/d/github/Basketball_Scraping/site/examples/player_comparison_examples.csv'
stat_options = ['PPG', 'APG', 'RPG', 'SPG', 'BPG', 'STOCKS_PG', 'FG%', 'FT%', '2P%', '3P%', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 
advanced_stat_options = ['TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'W%', 'EFG%', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_RATIO', 'TM_TOV%', 'PACE', 'PIE', 'POSS', 'POSS_PG']
xaxis = 'SEASON'
plot_number = 0

# READ IN THE TEAM COLORS
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)
emoji_df = pd.read_csv(emoji_file)
stat_df = pd.read_csv(stat_file)
examples_df = pd.read_csv(examples, sep='|')

# INITIAL SESSION STATE DEFAULTS
st.session_state['Player 1'] = 'LeBron James'
st.session_state['Player 2'] = 'Stephen Curry'
st.session_state['Stat'] = 'PPG'
st.session_state['Players'] = ['Stephen Curry', 'Chris Paul', 'Steve Nash']
st.session_state['Stat'] = 'PPG'
st.session_state['Stats'] = ['PPG', '3P%', 'FG%']
#st.session_state['compare_years'] = True
#st.session_state['advanced'] = False

# SETS THE OPTIONS FOR THE SELECTBOXES USING THE EXAMPLE DATAFRAME
def get_session_state_example(example=None):
    st.session_state['Example'] = example
    # get the players for the example
    players = examples_df[examples_df['Question'] == example]['Players'].values[0]
    st.session_state['Players'] = players
    # get the stats for the example
    stats = examples_df[examples_df['Question'] == example]['Stats'].values[0]
    st.session_state['Stats'] = stats
    if len(players) == 2 and len(stats) == 1:
        st.session_state['player_1'] = players[0]
        st.session_state['player_2'] = players[1]
        st.session_state['Stat'] = stats[0]
    if stats[0] in advanced_stat_options:
        st.session_state['advanced'] = True
    #st.session_state['compare_years'] = examples_df[examples_df['Question'] == example]['compare_years'].values[0]
    #st.session_state['advanced'] = examples_df[examples_df['Question'] == example]['advanced'].values[0]    

# READ IN THE EXAMPLES
if examples_df.empty == False:
    examples = examples_df['Question'].tolist()
    players, stats = examples_df['Players'].tolist(), examples_df['Stats'].tolist()
    players, stats = [player.split(', ') for player in players], [stat.split(', ') for stat in stats] 
    examples_df['Players'], examples_df['Stats'] = players, stats

    # pick a random number between 0 and the length of the examples
    example_index = 0
    if 'Example' not in st.session_state:
        random_example = random.choice(examples)
        example_index = examples.index(random_example)
        get_session_state_example(random_example)

# FUNCTIONS
graph_colors = ['#F27522', 'lightgrey', '#4082de', '#ADD8E6', '#F08080', '#FFA07A', '#FFE4B5', '#FF4500', '#FFD700', '#00FF00']
def compare_player_scatterplot(_player_dfs, _xaxis, _yaxis, n=0, colors=graph_colors):
    names, hover_templates = [], []
    for player_df in _player_dfs:
        names.append(player_df['PLAYER_NAME'].values[0])
    # make the hover template for the player name
    for player_df, name in zip(_player_dfs, names):
        hover_template = name + f'<br>AGE: ' + player_df['AGE'].astype(str) + f'<br>SEASON: ' + player_df['SEASON'].astype(str) + f'<br>#YEARS IN LEAGUE: ' + player_df["#YEARS IN LEAGUE"].astype(str) + '<br>' + _yaxis + ': ' + player_df[_yaxis].astype(str) + '<br>GP: ' + player_df['GP'].astype(str)
        hover_templates.append(hover_template)
    # check if colors is smaller than the number of players, if so, add more colors
    if len(colors) < len(_player_dfs):
        # add random colors to the list of colors
        for i in range(len(colors), len(_player_dfs)):
            colors.append('#' + ''.join([str(hex(mp.rand.randint(0, 255)))[2:] for _ in range(3)]))
    for player_df, hover_template, player_name, color in zip(_player_dfs, hover_templates, names, colors):
        # if the first player, create the fig
        if player_df['PLAYER_NAME'].values[0] == _player_dfs[0]['PLAYER_NAME'].values[0]:
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

def write_output_blurb(_dict, _stat):
    _dict = {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1][_stat], reverse=True)}
    # get the player with the highest average for the stat
    max_player = list(_dict.keys())[0]
    max_value = avg_dict[max_player][_stat]
    #st.write(f'🏀 **{max_player}** averaged :green[**{max_value} {_stat}**] during their career')
    st.write(f'🏀 **{max_player}** averaged :green[**{max_value} {_stat}**]')
    # calculate how much higher the max player is than the other players
    for player, value in avg_dict.items():
        if player != max_player:
            diff = round(max_value - value[_stat],3)
            st.write(f'🏀 **{player}** averaged :red[**{diff} {_stat}**] less than **{max_player}** **(:green[{value[_stat]} {_stat}])**')

def get_player_info_and_dfs(_season_dfs, _player_names_count, _players):
    # get the longest tenured player
    longest_tenured_player = _player_names_count[_player_names_count.index.isin(players)].idxmax()
    shortest_tenured_player = _player_names_count[_player_names_count.index.isin(players)].idxmin()
    output_dfs = []
    for player in _players:
        output_df = _season_dfs[_season_dfs['PLAYER_NAME'] == player].reset_index(drop=True)
        output_df['#YEARS IN LEAGUE'] = output_df['SEASON'].astype(int) - output_df['SEASON'].astype(int).min()
        output_dfs.append(output_df)
        if player == longest_tenured_player:
            max_years = output_df['#YEARS IN LEAGUE'].max()
        if player == shortest_tenured_player:
            max_years_short = output_df['#YEARS IN LEAGUE'].min()
    return output_dfs, max_years, max_years_short

def trim_dfs_and_get_average_stats(_player_dfs, _stats, _cols,_colors=graph_colors):
    output_player_dfs = []
    output_colors = []
    avg_dict = {}
    for player_df,color in zip(_player_dfs,_colors):
        player_df = player_df[_cols]
        if st.session_state['go_deeper'] == True:
            # keep only the rows where the year is in the range
            if st.session_state['compare_years'] == True:
                if player_df['#YEARS IN LEAGUE'].max() <= max_years:
                    player_df = player_df[(player_df['#YEARS IN LEAGUE'] >= st.session_state['year_range'][0]) & (player_df['#YEARS IN LEAGUE'] <= st.session_state['year_range'][1])]
        # remove any players that have no data in the range
        if player_df.empty == False:
            output_player_dfs.append(player_df)
            output_colors.append(color)
            player = player_df['PLAYER_NAME'].values[0]
            if player in emoji_df['PLAYER_NAME'].values:
                player = annotate_with_emojis(player, emoji_df)
            # get the average of the stat for the player
            stat_dict = {}
            for stat in _stats:
                avg = player_df[stat].mean().round(3)
                stat_dict[stat] = avg
            avg_dict[player] = stat_dict
    return output_player_dfs, output_colors, avg_dict

# END FUNCTIONS

# CHECKBOXES: GO DEEPER AND EXPLANATIONS
col1, col2 = st.columns(2)
with col1:
    go_deeper = st.checkbox(':grey[**Go Deeper**]', value=False, key='go_deeper')
with col2:
    explanations = st.checkbox(':grey[**Explanations**]', value=True, key='explanations')

# GET THE EXAMPLES IF GO DEEPER IS CHECKED
if go_deeper:
    left, right = st.columns(2, vertical_alignment='bottom') 
    random_example = None
    with right:
        if st.button('**Click to see an example**', key='example_checkbox'):
            random_example = random.choice(examples)
            example_index = examples.index(random_example)
            get_session_state_example(random_example)
        if 'index' not in st.session_state:
            st.session_state['index'] = None 
        if random_example is not None:
            st.session_state['index'] = examples.index(random_example)
    with left:
        example = st.selectbox('**Examples**', examples, index=st.session_state['index'], placeholder='pick something', key='example_selectbox')
        if st.session_state['example_selectbox'] != st.session_state['Example']:
            get_session_state_example(st.session_state['example_selectbox'])
    st.divider()

# TOGGLE FOR TRADITIONAL/ADVANCED STATS
if st.session_state['explanations'] == True:
    st.write('**Toggle to switch between :green[Traditional/Advanced] Stats**')
if st.toggle('**Advanced**', key='advanced', value=False):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
    stat_options = advanced_stat_options
    advanced = True
if st.session_state['go_deeper'] == True:
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
season_dfs = pd.DataFrame()
for key in year_data_dict.keys():
    # add the year column to the dataframe
    year_df = year_data_dict[key]
    year_df['YEAR'] = key
    season_dfs = pd.concat([season_dfs, year_df], ignore_index=True)
    
# check if the player name is duplicated, if so remove the duplicates
player_names_no_dups = season_dfs['PLAYER_NAME'].drop_duplicates(keep=False)
# if the player is in the list, remove them from the dataframe
season_dfs = season_dfs[~season_dfs['PLAYER_NAME'].isin(player_names_no_dups)]
# reset the index of the dataframe
season_dfs = season_dfs.reset_index(drop=True)
# count the number of instances of the player names in the dataframe
player_names_count = season_dfs['PLAYER_NAME'].value_counts()

# MAIN - PAGE SETUP BELOW
## PAGE BLURB
## SELECT PLAYERS
## TOGGLE TO PLOT BY YEARS IN LEAGUE OR SEASON
## SELECT STATS TO PLOT
## CHOOSE TO PLOT BY YEARS IN LEAGUE OR SEASON
## LOOP THROUGH THE STATS AND PLOT THEM AS SCATTERPLOTS

## PAGE BLURB
if st.session_state['explanations'] == True:
    if go_deeper:
        st.write('''
                **Now you can select up to :green[10 players] and :green[multiple stats] to plot**\n
                **You can also look at stints of careers by adjusting the :green[year] range**\n
                ''')
    else:
        st.write('''
                **Pick :grey[2 players] and :grey[1 stat] to plot on a line graph over time**\n
                 ''')
st.divider()

## SELECT PLAYERS
player_dfs = []
### IF GO DEEPER, SELECT MULTIPLE PLAYERS
if go_deeper:
    players = st.multiselect('**Select Players to Compare**', player_names_count.index.tolist(), default=st.session_state['Players'], key='players')
    # check if the players list is longer than 10
    if len(players) > 10:
        st.warning('*> 10 players may result in crashing, please select fewer players to compare*')
        st.stop()
    player_dfs, max_years, max_years_short = get_player_info_and_dfs(season_dfs, player_names_count, players)    

    ## SELECT STATS TO PLOT 
    # if advanced is False, pick from the traditional stats
    if st.session_state['advanced'] == False:
        stats = st.multiselect('**Select Stats to Compare**', stat_options, default=st.session_state['Stats'], key='stats')
    # if advanced is True, pick from the advanced stats
    else:
        stats = st.multiselect('**Select Stats to Compare**', advanced_stat_options, default=['TS%', 'USG%', 'AST%'], key='stats')

    ## CHOOSE TO PLOT BY YEARS IN LEAGUE OR SEASON
    if st.session_state['explanations'] == True:
        st.write('**Toggle to plot by #YEARS IN LEAGUE/SEASON**')
    if st.toggle('**Compare by #YEARS IN LEAGUE**', key='compare_years', value=True):
        xaxis = '#YEARS IN LEAGUE'
    if st.session_state['compare_years'] == True:
        # choose the year range to plot
        year_range = st.slider('**Select Year Range**', min_value=0, max_value=max_years, value=(0, max_years), key='year_range')
### IF NOT GO DEEPER, SELECT 2 PLAYERS, WITH BOXES SIDE BY SIDE
else:
    left, right = st.columns(2)
    # get the index for player 1 and player 2
    player_1_index, player_2_index = player_names_count.index.get_loc(st.session_state['Player 1']), player_names_count.index.get_loc(st.session_state['Player 2'])
    with left:
        player_1 = st.selectbox('**Player 1**', player_names_count.index.tolist(), index=player_1_index, key='player_1')
    with right:
        player_2 = st.selectbox('**Player 2**', player_names_count.index.tolist(), index=player_2_index, key='player_2')
    players = [player_1, player_2]
    for player in players:
        player_df = season_dfs[season_dfs['PLAYER_NAME'] == player].reset_index(drop=True)
        player_df['#YEARS IN LEAGUE'] = player_df['SEASON'].astype(int) - player_df['SEASON'].astype(int).min()
        player_dfs.append(player_df)
    # get the stat to plot
    stat1_index = stat_options.index(st.session_state['Stat'])
    stat1 = st.selectbox('**Select Stat**', stat_options, index=stat1_index, key='stat')
    stats = [stat1]

# ADD TO THE LIST OF COLUMNS TO KEEP
cols = ['PLAYER_NAME', 'AGE', 'SEASON', '#YEARS IN LEAGUE', 'GP']
for stat in stats:
    cols.append(stat)
st.divider()

# keep the first 3 columns and the stat columns
output_player_dfs, output_colors, avg_dict = trim_dfs_and_get_average_stats(player_dfs, stats, cols)

## LOOP THROUGH THE STATS AND PLOT THEM AS SCATTERPLOTS
if st.session_state['go_deeper'] == True:
    if st.session_state['explanations'] == True:
        if st.session_state['compare_years'] == True:
            st.write(f'**:green[{year_range[0]} - {year_range[1]}] YEARS IN THE LEAGUE**')
        else:
            st.write(f'**CAREER AVERAGES**')
    for stat in stats:
        compare_player_scatterplot(output_player_dfs, xaxis, stat, plot_number, output_colors)
        plot_number+=1
        if st.session_state['explanations'] == True:
            write_output_blurb(avg_dict, stat)
else:
    st.write(f'**CAREER AVERAGES | {player_1} vs {player_2}**')
    compare_player_scatterplot(output_player_dfs, xaxis, stat1, plot_number, output_colors)
    plot_number+=1
    if st.session_state['explanations'] == True:
        write_output_blurb(avg_dict, stat1)
st.divider()

# add a button to show the player data
st.expander('**Show Player Data**', expanded=False)
with st.expander('**Show player data**', expanded=False):
    columns = st.columns(len(output_player_dfs))
    for player_df, name, col in zip(output_player_dfs, players, columns):
        player_df = player_df.drop(columns=['PLAYER_NAME'])
        with col:
            st.write(f'**{name}**')
            st.dataframe(player_df, use_container_width=True, hide_index=True)

# PRINT OUT EMOJI PLAYERS
sum = len(players) + len(stats)
if st.session_state['go_deeper'] == True and sum >= 8 and st.session_state['explanations'] == False:
    emoji_players = emoji_df[emoji_df['PLAYER_NAME'].isin(players)]
    if len(emoji_players) > 0:
        st.expander(f'**Emojis**', expanded=True)
        with st.expander(f':rainbow[**Emojis**]', expanded=False):
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