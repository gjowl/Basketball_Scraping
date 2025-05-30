import streamlit as st
import os, pandas as pd
import plotly.express as px
from functions import sort_and_show_data, change_to_team_colors,plot_quadrant_scatter, create_year_data_dict, annotate_with_emojis,emoji_check
import random

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
emoji_file = '/mnt/d/github/Basketball_Scraping/site/emoji_players.csv'
stat_file = '/mnt/d/github/Basketball_Scraping/site/stats.csv'
example_file = '/mnt/d/github/Basketball_Scraping/site/examples/season_stats_examples.csv'
stat_options = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'STOCKS_PG', 'FG%', 'FT%', '2P%', '3P%', 'OREB_PG', 'DREB_PG', 'AST_TO', 'TOV_PG', 'FTA_PG', '3PM_PG', '3PA_PG', '2PM_PG', '2PA_PG', 'NBA_FANTASY_PTS_PG'] 
advanced_stat_options = ['TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'W%', 'EFG%', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_RATIO', 'TM_TOV%', 'PACE', 'PIE', 'POSS', 'POSS_PG']
expander_color = ':green'
stat_color = ':blue'
top_players_color = ':violet'
default_num_gp = 65
max_players = 30
descriptor = 'Top'

# BOOL
advanced = False
go_deeper = False
explanation = False
flip_top = False

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)
emoji_df = pd.read_csv(emoji_file)
stat_df = pd.read_csv(stat_file)
example_df = pd.read_csv(example_file, sep='|')

# SETS THE OPTIONS FOR THE SELECTBOXES USING THE EXAMPLE DATAFRAME
def get_session_state_example(example=None):
    st.session_state['Example'] = example
    # get the players for the example
    season = example_df[example_df['Question'] == example]['Season'].values[0]
    st.session_state['season_selectbox'] = season 
    # get the stats for the example
    stat = example_df[example_df['Question'] == example]['Stat'].values[0]
    num_players = int(example_df[example_df['Question'] == example]['Number of Players'].values[0])
    age_range = example_df[example_df['Question'] == example]['Age Range'].values[0]
    age_range = [int(age_range[0]), int(age_range[1])]
    #st.write(st.session_state['age_range'])
    st.session_state['age_range'] = age_range
    st.session_state['num_players'] = num_players
    if stat in advanced_stat_options:
        st.session_state['advanced_toggle'] = True
    else:
        st.session_state['advanced_toggle'] = False
    st.session_state['stat_selectbox'] = stat

# SESSION STATE
if 'Emojis Unlocked' not in st.session_state:
    st.session_state['Emojis Unlocked'] = False

# READ IN THE EXAMPLES
if example_df.empty == False:
    examples = example_df['Question'].tolist()
    season = example_df['Season'].values[0]
    stat = example_df['Stat'].values[0]
    age_range = example_df['Age Range'].tolist()
    age_range = [age.split(', ') for age in age_range] 
    example_df['Age Range'] = age_range

    # pick a random number between 0 and the length of the example
    example_index = 0
    if 'Example' not in st.session_state:
        random_example = random.choice(examples)
        example_index = examples.index(random_example)
        get_session_state_example(random_example)

# FUNCTIONS
def show_stat_explanation_expander(_stat_df):
    stat_explanation = st.expander(':green[**Traditional/Advanced Stats**]', expanded=False)
    with stat_explanation:
        click_me = st.checkbox('**click me :D**', value=False, key='click_me')
        stat_types = _stat_df['Type'].unique()
        for type in stat_types:
            stat_type_df = _stat_df[_stat_df['Type'] == type]
            st.write(f'**{type} Stats**')
            for index, row in stat_type_df.iterrows():
                stat_type = row['Type']
                if stat_type == 'Traditional':
                    st.write(f'🏀 **{row["Stat"]}** - [{row["Definition"]}]({row["Link"]})')
                else:
                    st.write(f'🏀 **{row["Stat"]}** - [{row["Definition"]}]({row["Link"]})')

# CHECKBOX FOR MORE OPTIONS AND EXPLANATIONS
go_deeper_variable_color = ':grey'
cols = st.columns(2)
with cols[0]:
    go_deeper = st.checkbox(f'**{go_deeper_variable_color}[Go Deeper]**', value=False, key='go_deeper')
    if st.session_state['go_deeper'] == True:
        go_deeper_variable_color = ':green'
with cols[1]:
    explanation = st.checkbox(f'**:grey[Explanations]**', value=True, key='explanations')

# GET THE EXAMPLE: FIXED THIS ON 2025-05-06 TO WORK MORE SEEMLESSLY
if st.session_state['go_deeper'] == True:
    left, right = st.columns(2, vertical_alignment='bottom')
    with right:
        random_example = None
        if st.button('**Click to see an example**', key='example_checkbox'):
            random_example = random.choice(examples)
            example_index = examples.index(random_example)
            #get_session_state_example(random_example)
            st.session_state['example_selectbox'] = random_example
            #st.session_state
        if 'index' not in st.session_state:
            st.session_state['index'] = None 
        if random_example is not None:
            st.session_state['index'] = examples.index(random_example)
    with left:
        example = st.selectbox('**Examples**', examples, index=st.session_state['index'], placeholder='pick something', key='example_selectbox')
        if st.session_state['example_selectbox'] != st.session_state['Example'] and st.session_state['index'] != None:
            get_session_state_example(st.session_state['example_selectbox'])

# INTRO BLURB
if st.session_state['explanations'] == True:
    if st.session_state['go_deeper'] == False:
        st.write('''
                **Pick the :violet[number of players] and the stat you want to see, and the top players will be plotted in a bar graph.**\n
                ***Data from present to the 1996-97 season.***\n
                \n
        ''')
    else:
        st.write(f'''
                **Pick the :violet[number of players], :green[games played], and the :green[age range] of players.**\n
                **Then pick two stats you want to graph, and the top players will be plotted in scatterplots.**\n
                ***Data from present to the 1996-97 season.***\n
                \n
        ''')
st.divider()

## TOGGLE FOR TRADITIONAL/ADVANCED STATS
if st.session_state['go_deeper'] == True:
    show_stat_explanation_expander(stat_df)

## TOGGLE FOR ADVANCED STATS
if st.session_state['explanations'] == True:
    st.write('**Toggle to switch between :green[Traditional/Advanced] Stats**')
if st.toggle('**Advanced**', value=False, key='advanced_toggle'):
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
    stat_options = advanced_stat_options

# LOAD IN THE DATA
year_data_dict = create_year_data_dict(datadir)
# flip the dict to get the most recent season first
year_data_dict = {k: year_data_dict[k] for k in sorted(year_data_dict.keys(), reverse=True)}
left, right = st.columns(2)
with left:
    season = st.selectbox('**Season**', year_data_dict.keys(), index=0, placeholder='Season...', key='season_selectbox')
if season is None:
    st.warning('*Please select a season (data back to the 1996-97 season)*')
    st.stop()
data = year_data_dict[season]
max_gp = data['GP'].max()

# MAIN
## PAGE SETUP BELOW
## SELECT THE NUMBER OF PLAYERS AND GP TO FILTER 
## SELECT THE STAT/STATS TO PLOT
## BAR GRAPH PLOT AND OUTPUTS

## SELECT THE NUMBER OF PLAYERS AND GP TO FILTER 
if st.session_state['go_deeper'] == True:
    max_players = 100
num_players = st.slider('***Number of players to show***', 1, max_players, 10, key='num_players')
num_gp = default_num_gp 
if st.session_state['go_deeper'] == True:
    num_gp = st.slider('***Minimum number of games played****', 1, max_gp, default_num_gp, key='num_gp')
    min_age, max_age = data['AGE'].min(), data['AGE'].max()
    ages = st.slider('***Age Range***', min_age, max_age, (min_age, max_age), format='%d', key='age_range')
    data = data[(data['AGE'] >= ages[0]) & (data['AGE'] <= ages[1])]
    go_deeper = True
# check if there are less than num_players in the data
if len(data) < num_players:
    num_players = len(data)
st.divider()

## SELECT THE STAT TO PLOT
cols = data.columns.tolist()
# IF GO DEEPER AND CLICK ME ARE TRUE, THEN ADD THE HIDDEN TOGGLE TO LOOK AT BOTTOM PLAYERS
if st.session_state['go_deeper'] == True and st.session_state['click_me'] == True:
    flip_top = st.toggle(f'{go_deeper_variable_color}[**Flip Top**]', value=False, key='flip_top')
    if flip_top == True:
        descriptor = 'Bottom'

# WRITE THE EXPLANATION FOR WHAT TO DO IF GO DEEPER IS TRUE (DIFFERENT COLORS AND LONGER EXPLANATION)
stat_options = [col for col in stat_options if col in cols]
if st.session_state['go_deeper'] == True and st.session_state['explanations'] == True:
    stat_options = [col for col in stat_options if col in cols]
    st.write(f'Choose a second stat to plot the :violet[**{descriptor} {num_players}**] players who played at least {go_deeper_variable_color}[**{num_gp} games**] and are between ages {go_deeper_variable_color}[**{int(ages[0])} and {int(ages[1])}**]')
# IF GO DEEPER IS FALSE, THEN WRITE THE EXPLANATION FOR WHAT TO DO
elif st.session_state['explanations'] == True:
    st.write(f'Choose a stat to plot the :violet[**{descriptor} {num_players}**] players who played at least :grey[**{num_gp} games**]')
with right:
    stat = st.selectbox('**Stat**', stat_options, index=1, placeholder='Statistic...', key='stat_selectbox')
if stat is None:
    st.warning('*Please select a stat to plot*')
    st.stop()

# check if the stat is in the options list
if stat not in option_df['OPTION'].tolist():
    y_axis = 'MPG'
else:
    y_axis = option_df[option_df['OPTION'] == stat]['SORT'].values[0]
if st.session_state['go_deeper'] == True:
    stat_options_2 = stat_options.copy()
    stat_options_2.remove(stat)
    default_index = stat_options_2.index(y_axis)
    stat_2 = st.selectbox('**y-axis**', stat_options_2, index=default_index, placeholder='Statistic...')
    y_axis = stat_2
## keep only the nubmer of games played
data = data[data['GP'] >= num_gp]
st.divider()

### calculate percentiles for the option
data[f'Percentile'] = data[stat].rank(pct=True)

## BAR GRAPH PLOT AND OUTPUTS
top_players, bar_graph = sort_and_show_data(data, stat, team_colors, descriptor, flip_top, num_players) # plots the top player bar graph and scatter plot
st.plotly_chart(bar_graph, use_container_width=True)
output_df = top_players.copy()
output_df = output_df[['PLAYER_NAME', 'GP', stat, 'TEAM_ABBREVIATION']]
if st.session_state['go_deeper'] == False:
    top_players_by_age = top_players.sort_values(by='AGE', ascending=True)
    if top_players_by_age.empty:
        st.write('**No players found with the selected filters, try lowering the number of GP!**')
        st.stop()
    emoji_df = emoji_check(emoji_df, top_players_by_age)
    # get the youngest and oldest players
    young_player = top_players_by_age.iloc[0]['PLAYER_NAME']
    old_player = top_players_by_age.iloc[-1]['PLAYER_NAME']
    if young_player in emoji_df['PLAYER_NAME'].tolist():
        young_player = annotate_with_emojis(young_player, emoji_df)
    if old_player in emoji_df['PLAYER_NAME'].tolist():
        old_player = annotate_with_emojis(old_player, emoji_df)
    if st.session_state['explanations'] == True:
        st.write(f'''
                The youngest player in the :violet[**{descriptor} {num_players}**] is **{young_player}** at {go_deeper_variable_color}[**{int(top_players_by_age.iloc[0]['AGE'])}**] years old, averaging {expander_color}[**{round(top_players_by_age.iloc[0][stat],1)} {stat}**]\n 
                The oldest player in the :violet[**{descriptor} {num_players}**] is **{old_player}** at {go_deeper_variable_color}[**{int(top_players_by_age.iloc[-1]['AGE'])}**] years old, averaging {expander_color}[**{round(top_players_by_age.iloc[-1][stat],1)} {stat}**]\n
                 ''')
    # check if there are any non-unique TEAM_ABBREVIATION values in the top players
    team_counts = top_players['TEAM_ABBREVIATION'].value_counts()
    if len(team_counts) > 1:
        for team, count in team_counts.items():
            if count > 1:
                players = top_players[top_players['TEAM_ABBREVIATION'] == team]['PLAYER_NAME'].values
                for player in players:
                    if player in emoji_df['PLAYER_NAME'].tolist():
                        output_player = annotate_with_emojis(player, emoji_df)
                        players[players == player] = output_player
                if explanation == True:
                    st.write(f':red[**{team}**] has multiple players in the :violet[**{descriptor} {num_players}**] - **{", ".join(players)}**')
    # EXPANDER FOR THE DATA
    st.expander(f'**{descriptor} Players Data**', expanded=False)
    with st.expander(f'**{descriptor} Players Data**', expanded=False):
        st.dataframe(output_df, use_container_width=True, hide_index=True)
        if young_player in emoji_df['PLAYER_NAME'].tolist():
            young_player = annotate_with_emojis(young_player, emoji_df)
        if old_player in emoji_df['PLAYER_NAME'].tolist():
            old_player = annotate_with_emojis(old_player, emoji_df)
    st.divider()

# MORE OPTIONS INCLUDES THE ADDITION OF THE SCATTERPLOT
if st.session_state['go_deeper'] == True:
    data = data.sort_values(by=y_axis, ascending=flip_top)
    data.reset_index(drop=True, inplace=True)
    # plot the quadrant graph with the stat vs the y_axis
    plot_quadrant_scatter(data, stat, y_axis, top_players, team_colors)
    scatter_data = data[['PLAYER_NAME', 'GP', stat, y_axis, 'TEAM_ABBREVIATION']].copy()
    scatter_data.sort_values(by=stat, ascending=flip_top, inplace=True)
    x_avg, y_avg = round(data[stat].mean(),2), round(data[y_axis].mean(),2)

    # if explanations is true, show the explanation for the scatter plot
    if st.session_state['explanations'] == True:
        st.write(f'''
                The :blue[**{stat}**] vs :red[**{y_axis}**] scatter plot shows the distribution of players in the league for the :green[**{season} season**]. \n
                The :violet[{descriptor} {num_players}] players are highlighted by their team colors in the scatter plot, and all other players are plotted in gray. \n
                The red and blue dashed lines represent the :green[**{season} season**] averages: \n 
                🏀 **:red[Avg {stat} = {x_avg}]** \n
                🏀 **:blue[Avg {y_axis} = {y_avg}]** \n
                Typically, the best players are found in the top right quadrant, being above average for both stats. \n
                Hover over a point to see the player name, team, and the **:green[**{season} season**]** averages ! \n
                 ''')
    
    # add the player data as an expander
    st.expander(f'**{descriptor} Players Data**', expanded=False)
    with st.expander(f'**{expander_color}[{descriptor} Players Scatter Data]**', expanded=False):
        st.write(f'''
            The :blue[**x-axis**] is the :blue[**{stat}**] and the :red[**y-axis**] is the :red[**{y_axis}**], with the **{season} season** average plotted along the axes in red \n
            The red and blue dashed lines represent the :green[**{season} season**] averages: \n 
            🏀 **:red[Avg {stat} = {x_avg}]** \n
            🏀 **:blue[Avg {y_axis} = {y_avg}]** \n
             ''')
        output_data = scatter_data.head(num_players)
        st.dataframe(output_data, use_container_width=True, hide_index=True)
        emoji_player_list = []
        for player in output_data['PLAYER_NAME']:
            if player in emoji_df['PLAYER_NAME'].tolist():
                player_emoji = annotate_with_emojis(player, emoji_df)
                emoji_player_list.append(player_emoji)
        st.write(f':rainbow[**Emoji Players Found!**] {" | ".join(emoji_player_list)}')
    st.divider()

# SHOW ALL DATA
st.expander('**Show All Data**', expanded=False)
with st.expander(f'**Show All Data**', expanded=False):
    if st.toggle('**Simplified Data**', key='show_all_data', value=True):
        data = data[['PLAYER_NAME', 'GP', stat, y_axis, 'TEAM_ABBREVIATION']].copy()
        data.sort_values(by=stat, ascending=flip_top, inplace=True)
        st.dataframe(data, use_container_width=True, hide_index=True)
    else:
        st.dataframe(data, use_container_width=True, hide_index=True)

## ADD IN THE EMOJIS
if st.session_state['go_deeper'] == True and st.session_state['click_me'] == True and st.session_state['explanations'] == True:
    if st.session_state['Emojis Unlocked'] == False:
        st.session_state['Emojis Unlocked'] = True
        st.toast('**Emojis Unlocked! Check the bottom of the page :D**')
        st.toast("おめでとうございます,絵文字を見つけました")
    st.expander('**Emojis**', expanded=False)
    with st.expander(f':rainbow[**Emojis**]', expanded=False):
        if len(emoji_df) > 0:
            player_emoji_list = []
            emoji_df = emoji_check(emoji_df, data)
            for player in emoji_df['PLAYER_NAME']:
                player_emoji = annotate_with_emojis(player, emoji_df)
                player_emoji_list.append(player_emoji)
            st.write(f'{" | ".join(player_emoji_list)}')
        if num_gp == 1 and min_age == ages[0] and max_age == ages[1]:
            st.write(f'''
            "O-me-de-tou-go-za-i-mas,E-mo-ji o mi-tsu-ke-ma-shi-ta" - "Congrats, you found the emojis"\n
            These are all the emojis present in data for the **:green[{season} season]** :D\n
            ''')