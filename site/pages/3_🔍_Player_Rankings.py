import streamlit as st
import os, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functions import emoji_check, annotate_with_emojis, create_year_data_dict
import random

# SET PAGE CONFIG
st.set_page_config(page_title='Player Rankings',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('🔍 Player Rankings')

# VARIABLES 
cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
#datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
#contains = 'all_game' # file you want to read
datadir = f'{cwd}/site/NBA_API_DATA/BOXSCORES'
advanced_datadir = f'{cwd}/site/NBA_API_DATA/ADVANCED'
contains = '2023-24_boxscore' # file you want to read
colors = f'{cwd}/site/team_colors_hex.csv'
options = f'{cwd}/site/options.csv'
emoji_file = f'{cwd}/site/emoji_players.csv'
stat_file = f'{cwd}/site/stats.csv'
go_deeper = False
all_time = True
season = '2024-25'
start_player = 'LeBron James'

# 
cols = st.columns(2)
with cols[0]:
    go_deeper = st.checkbox('**:grey[Go Deeper]**', value=False, key='go_deeper')
with cols[1]:
    explanation = st.checkbox('**:grey[Explanations]**', value=True, key='explanations')

# read in the team colors
team_colors = pd.read_csv(colors)
option_df = pd.read_csv(options)
emoji_df = pd.read_csv(emoji_file)

## VARIABLES FOR THE STATS TO GET
name_and_year = ['PLAYER_NAME', 'YEAR']
cols_to_keep = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MPG'] # keep the player name, team abbreviation, and GP
shooting = ['FG%', 'FGA_PG', 'FGM_PG', '2P%', '2PA_PG', '2PM_PG', '3P%', '3PA_PG', '3PM_PG', 'FT%', 'FTA_PG', 'FTM_PG'] # make into quadrant plots
traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'STOCKS_PG', 'TOV_PG', 'PF_PG']
advanced = ['AST_TO', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%']
# TODO: get a team count stat as well
rank_cols = [traditional, shooting, advanced]
check_gp = False
gp, plot_number = 0, 0

# FUNCTIONS
def get_ranks(_data, _stat_list, _season=True):
    player_ranks = pd.DataFrame()
    for stat in _stat_list:
        if player_ranks.empty:
            if _season == False:
                player_ranks = _data[['PLAYER_NAME', 'TEAM_ABBREVIATION']].copy()
            else: 
                # add the player name and year to the dataframe
                player_ranks = _data[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'SEASON', 'YEAR']].copy()
        # calculate the percentile for each stat
        _data[f'{stat}_Percentile'] = _data[stat].rank(pct=True)
        # create a ranked list column based on the percentile of the stat
        _data[f'{stat}_Rank'] = _data[stat].rank(method='first', ascending=False)
        player_ranks = pd.concat([player_ranks, _data[[f'{stat}_Percentile', f'{stat}_Rank']]], axis=1)
    return player_ranks

# get the player rankings for each season
@st.fragment
def get_season_player_rankings(_year_data_dict, _advanced_data_dict, _rank_cols, _check_gp, _gp):
    output_dfs = []
    # go through the columns to rank
    for ranks in _rank_cols:
        # get the player rankings for the season
        tmp_df = pd.DataFrame()
        for key in _year_data_dict.keys():
            season_df = _year_data_dict[key].copy()
            # to get advanced data
            if 'TS%' in ranks:
                season_df = _advanced_data_dict[key].copy()
            if _check_gp:
                # keep only the players who have played at least _gp games
                season_df = season_df[season_df['GP'] >= _gp]
            player_ranks = get_ranks(season_df, ranks)
            tmp_df = pd.concat([tmp_df, season_df], ignore_index=True)
        output_dfs.append(tmp_df) 
    return output_dfs

@st.fragment
# get the all time player rankings
def get_all_time_player_rankings(_year_data_dict, _advanced_data_dict, _rank_cols, _check_gp, _gp, _years_count=None):
    output_dfs = []
    for ranks in _rank_cols:
        # get the player rankings for the season
        tmp_df = pd.DataFrame()
        for key in _year_data_dict.keys():
            season_df = _year_data_dict[key]
            # to get advanced data
            if 'TS%' in ranks:
                season_df = _advanced_data_dict[key]
            if _check_gp:
                # keep only the players who have played at least _gp games
                season_df = season_df[season_df['GP'] >= _gp]
            tmp_df = pd.concat([tmp_df, season_df], ignore_index=True)
        # get the mean for each stat in the rank list
        avg_df = tmp_df.groupby('PLAYER_NAME')[ranks].mean().reset_index()
        # sort by SEASON
        avg_df = avg_df.sort_values(by='SEASON', ascending=True).reset_index(drop=True)
        # replace team abbreviation with the first team played for
        avg_df['TEAM_ABBREVIATION'] = tmp_df.groupby('PLAYER_NAME')['TEAM_ABBREVIATION'].first().values
        # internally rids of players who have not had enough years in the league
        if _years_count is not None:
            avg_df['YEARS_COUNT'] = tmp_df.groupby('PLAYER_NAME')['YEAR'].count().values
            avg_df = avg_df[avg_df['YEARS_COUNT'] >= _years_count]
        tmp_ranks = get_ranks(avg_df, ranks, _season=False)
        output_dfs.append(avg_df)
    return output_dfs

# transform the ranks for plotting
@st.fragment
def transform_ranks_for_plotting(_df):
    # separate by _ into index and stat
    ranks, percentiles = _df.columns[_df.columns.str.contains('_Rank')].tolist(), _df.columns[_df.columns.str.contains('_Percentile')].tolist() 
    # separate ranks by _
    ranks, percentiles = [rank.split('_Rank')[0] for rank in ranks], [percentile.split('_Percentile')[0] for percentile in percentiles]
    player_ranks = pd.DataFrame()
    for stat in ranks:
        player_ranks[stat] = [_df[f'{stat}_Percentile'].values[0], _df[f'{stat}_Rank'].values[0], _df[f'{stat}'].values[0]]
    player_ranks = player_ranks.T
    player_ranks.columns = ['Percentile', 'Rank', 'Value']
    return player_ranks

# create a bar graph of the player ranks
def create_player_rank_bar_graph(_season_df, _player_ranks, _player, _title, _team_colors):
    # create hovertext with index: value
    hovertext = [f'{_player_ranks.index[i]}: {_player_ranks["Value"][i]}<extra></extra>' for i in range(len(_player_ranks))]
    # create a bar graph of the stat with the rank above the bar for the chosen player, with the value column as the hover text
    fig = go.Figure(data=[go.Bar(x=_player_ranks.index, y=_player_ranks['Percentile'], hovertemplate=hovertext)])
    # add the rank above each bar
    for i in range(len(_player_ranks)):
        # if ranking is NaN, skip it
        if pd.isna(_player_ranks['Rank'][i]):
            continue
        fig.add_annotation(x=i, y=_player_ranks['Percentile'][i], text=f'#{int(_player_ranks["Rank"][i])}', showarrow=False, font=dict(size=16), yshift=10)
    # remove the x-axis title
    fig.update_xaxes(title='')
    # set the x-axis label size
    fig.update_xaxes(tickfont=dict(size=16))
    fig.update_layout(font_family="monospace")
    # change the color of the bars to be the team color
    color1 = _team_colors[_team_colors['TEAM_ABBREVIATION'] == _season_df[_season_df['PLAYER_NAME'] == _player]['TEAM_ABBREVIATION'].values[0]]['Color 1'].values[0]
    color2 = _team_colors[_team_colors['TEAM_ABBREVIATION'] == _season_df[_season_df['PLAYER_NAME'] == _player]['TEAM_ABBREVIATION'].values[0]]['Color 2'].values[0]
    fig.update_traces(marker=dict(color=color1, line=dict(width=3, color=color2)))
    # remove the y-axis lines, title, and ticks
    fig.update_layout(yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), xaxis=dict(showgrid=False, zeroline=False, showticklabels=True))
    fig.update_yaxes(showline=False, title='', ticks='', showticklabels=False)
    # add a line at the 0 mark on the y-axis
    fig.add_hline(y=0, line_color=color2, line_width=3)
    #fig.update_traces(hovertemplate='%{x} Percentile: %{y:.3f}')
    st.plotly_chart(fig, use_container_width=True, key=f'player_rank_bar_graph_{plot_number}')

# merge rank dataframes together
@st.fragment
def merge_rank_dfs(_dfs):
    output_df = pd.DataFrame()
    for df in _dfs:
        if output_df.empty:
            output_df = df.copy()
        else:
            output_df = pd.merge(output_df, df, on=['PLAYER_NAME', 'TEAM_ABBREVIATION'])
    return output_df

# function to join the season ranks and averages dataframes (slightly annoying to do)
@st.fragment
def join_season_dfs(_data_dfs):
    output_df = pd.DataFrame()
    cols = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'YEAR', 'SEASON']
    for avg_df in _data_dfs:
        if output_df.empty:
            output_df = avg_df.copy()
        else:
            output_df.set_index(cols, inplace=True)
            tmp_avg_df = avg_df.copy()
            tmp_avg_df.set_index(cols, inplace=True)
            output_df = output_df.join(tmp_avg_df, lsuffix='_tmp', rsuffix='_tmp_2', how='outer').reset_index()
    # cols to drop from the ranks df,  
    contain_cols = '_tmp_2|AGE_tmp|MPG_tmp|FG%_tmp|FGM_PG_tmp|FGA_PG_tmp|AST_TO_tmp'
    output_df = output_df.loc[:, ~output_df.columns.str.contains(contain_cols)]
    output_df.columns = [col.split('_tmp')[0] for col in output_df.columns]
    return output_df 

def get_rank_player_data(_all_data, _player):
    player_dfs = []
    for df in _all_data:
        player_df = df[df['PLAYER_NAME'] == _player].reset_index(drop=True)
        player_dfs.append(player_df)
    return player_dfs

def get_years_in_league(_year_data_dict):
    # get the player rankings for the season
    tmp_df = pd.DataFrame()
    for key in _year_data_dict.keys():
        season_df = _year_data_dict[key].copy()
        # to get advanced data
        tmp_df = pd.concat([tmp_df, season_df], ignore_index=True)
    # get the years in the league for each player
    player_years = tmp_df[['PLAYER_NAME', 'YEAR']].copy()
    count_df = player_years.groupby('PLAYER_NAME')['YEAR'].count().reset_index()
    count_df = count_df.rename(columns={'YEAR': 'YEARS_IN_LEAGUE'})
    player_years = pd.merge(player_years, count_df, on='PLAYER_NAME', how='left')
    return player_years

# EXPLANATIONS
def tab1_explanation():
    if st.session_state['go_deeper']:
        st.write('''
                **Choose a player and season below to see their \*ranks in the given season**\n
                ''')
        st.caption('''
                **\*Ranks calculated for data back to the 1996-97 season**\n
                ''')
    else:
        st.write('''
                **Choose a player and see their rank in all available stats**\n
                ''')

# MAIN
## LOAD IN THE DATA
## SELECT A PLAYER FROM THE DROPDOWN
## TABS SEPARATED STATS AND GRAPHS
## BUTTON TO SHOW PLAYER DATA

# LOAD IN THE DATA
year_data_dict, advanced_data_dict = create_year_data_dict(datadir), create_year_data_dict(advanced_datadir)
## get all the unique player names from the year_data_dict
player_names_df = pd.DataFrame()
for key in year_data_dict.keys():
    # add the player name and season to the dataframe
    player_names_df = pd.concat([player_names_df, year_data_dict[key][['PLAYER_NAME', 'YEAR']].copy()], ignore_index=True)
player_names = player_names_df['PLAYER_NAME'].unique()
# if not going deeper, get the player names for the current season only
if st.session_state['go_deeper'] == False:
    player_names = player_names_df[player_names_df['YEAR'] == season]['PLAYER_NAME'].unique()

# get the years in the league for each player
all_player_years = get_years_in_league(year_data_dict)

# get the ranks for seasons and all time
season_rank_list = get_season_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp)
all_rank_list = get_all_time_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp)

## TABS START HERE
tabs = st.tabs(['**Player Search**', '**Rank Finder**'])

# TAB 1: PLAYER SEARCH
found_emojis = pd.DataFrame()
my_bar = st.progress(0, text='Loading...')
with tabs[0]:
    # variables
    titles = ['Traditional', 'Shooting', 'Advanced']

    # START HERE: Turn this into a function that can be rerun with a button, potentially a fragment
    left, right = st.columns(2, vertical_alignment='bottom')
    if st.session_state['go_deeper']:
        left, middle, right = st.columns(3, vertical_alignment='bottom')
    if st.session_state['explanations']: 
        tab1_explanation()
    my_bar.progress(10, text='Loading...')

    ## SELECT A PLAYER FROM THE DROPDOWN
    with right:
        if st.button('**Random Player**', key=f'random_player'):
            player_index = random.randint(0, len(player_names)-1)
            player = player_names[player_index]
            st.session_state['player'] = player
    with left:
        player = st.selectbox('**Select a Player**', player_names, index=player_names.tolist().index(start_player), placeholder='Player Name...', key=f'player')
    my_bar.progress(25, text='Loading...')

    # check if the player is in the emoji_df
    player_emoji = annotate_with_emojis(player, emoji_df)
    if player_emoji != player:
        found_emojis['PLAYER_NAME'] = player_emoji
        with st.sidebar:
            st.caption(player_emoji)
            #player = st.selectbox('**Select a Player**', player_names, index=player_names.tolist().index(start_player), placeholder='Player Name...', key=f'player_sidebar')
    player_rank_dfs = get_rank_player_data(season_rank_list, player)
    
    # reverse the list to get the most recent season first
    season_list = sorted(player_rank_dfs[0]['YEAR'].unique(), reverse=True) 
    #status.update(label=f'**{player_emoji}** ranks calculated!', state='complete')
    my_bar.progress(50, text='Loading...')

    # go deeper into the stats
    if st.session_state['go_deeper']:
        # add a season select box to choose the season to show the ranks for
        with middle:
            season = st.selectbox('**Select the Season**', season_list, key=f'season_{plot_number}')
        # remove players who have played less than the minimum games played in the season
        check_gp = st.checkbox('**:green[Games Played] Filter**', value=False)
        if check_gp:
            gp = st.slider('Number of games played', 0, 82, 65)
            player_gp = player_rank_dfs[0][player_rank_dfs[0]['YEAR'] == season]['GP'].max()
            if player_gp < gp:
                st.warning(f'{player_emoji} only played {player_gp} games in the {season} season.')
                with st.spinner(text=f'**loading ranks for players who played <= {player_gp} games...**') as status:
                    season_rank_list = get_season_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, player_gp)
                    all_rank_list = get_all_time_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, player_gp)
    st.divider()
    my_bar.progress(75, text='Loading...')

    # plot the player ranks for the season as bar graphs
    st.expander(f'**{player_emoji}**', expanded=False)
    with st.expander(f'**{player_emoji} {season} Season Ranks**', expanded=False):
        for ranks,rank_df,title in zip(rank_cols, player_rank_dfs, titles):
            player_df = rank_df[rank_df['PLAYER_NAME'] == player].reset_index(drop=True)
            season_df = player_df[player_df['YEAR'] == season].reset_index(drop=True)
            player_gp = season_df['GP'].max()
            player_ranks = transform_ranks_for_plotting(season_df) 
            create_player_rank_bar_graph(season_df, player_ranks, player, title, team_colors) 
            season_df = season_df[[col for col in season_df.columns if '_Percentile' not in col and '_Rank' not in col]]
            # show the player data in a table
            season_df = season_df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP'] + ranks]
            season_df[ranks] = season_df[ranks].round(2)
            st.dataframe(season_df, use_container_width=True, hide_index=True)
            plot_number += 1
    my_bar.progress(90, text='Loading...')

    # OUTPUT THE ALL TIME RANKS FOR THE PLAYER INTO AN EXPANDER
    st.expander('**All Time**', expanded=False)
    with st.expander(':rainbow[**All Time**]', expanded=False):
        # TODO: add a choice for team color here; maybe pills?
        if explanation:
            st.write(f'*TEAM COLOR IS THE FIRST TEAM PLAYED FOR')
            st.write(f'')
        for avg_df,title in zip(all_rank_list,titles):
            player_df = avg_df[avg_df['PLAYER_NAME'] == player].reset_index(drop=True)
            player_ranks = transform_ranks_for_plotting(player_df) 
            create_player_rank_bar_graph(player_df, player_ranks, player, title, team_colors) 
            # remove _Percentile and _Rank from the columns
            player_df = player_df[[col for col in player_df.columns if '_Percentile' not in col and '_Rank' not in col]]
            # round all but player name and team abbreviation to 2 decimal places
            cols = player_df.columns.tolist()
            cols = [col for col in cols if col not in ['PLAYER_NAME', 'TEAM_ABBREVIATION']]
            player_df[cols] = player_df[cols].round(2)
            st.dataframe(player_df, use_container_width=True, hide_index=True)
            plot_number += 1
    my_bar.progress(100, text='Loading...')
    st.expander(f'**{player_emoji}** All Data', expanded=False)
    with st.expander(f'**{player_emoji} All Data**', expanded=False):
        # remove _Percentile and _Rank from the columns
        output_df, df_list = pd.DataFrame(), []
        for player_rank_dfs in season_rank_list:
            player_df = player_rank_dfs[player_rank_dfs['PLAYER_NAME'] == player].reset_index(drop=True)
            player_df = player_df[[col for col in player_df.columns if '_Percentile' not in col and '_Rank' not in col and '_RANK' not in col]]
            # sort the dataframe by the season
            player_df = player_df.sort_values(by=['SEASON'], ascending=True).reset_index(drop=True)
            df_list.append(player_df)
        # merge the dataframes together
        output_df = join_season_dfs(df_list)
        # round all but player name and team abbreviation to 2 decimal places
        cols = output_df.columns.tolist()
        cols = [col for col in cols if col not in ['PLAYER_NAME', 'TEAM_ABBREVIATION']]
        output_df[cols] = output_df[cols].round(2)
        st.dataframe(output_df, use_container_width=True, hide_index=True)
my_bar.empty()

# TAB 2: STAT SEARCH
# merge dataframes for finding ranks
season_avg_df = join_season_dfs(season_rank_list)
all_rank_list_df = merge_rank_dfs(all_rank_list)
reset = False
# get the stat list
all_rank_cols = pd.concat(season_rank_list, ignore_index=True)
stat_list = all_rank_cols.columns[all_rank_cols.columns.str.contains('_Rank')].tolist()
# remove rank from the stat list
stat_list = [stat.split('_Rank')[0] for stat in stat_list]
with tabs[1]:
    if st.session_state['explanations']:
        if st.session_state['go_deeper'] == False:
            st.write('''
                    **Choose a stat to see where the player ranks in the league this season.**\n
                    ''')
    # go deeper into the stats
    if st.session_state['go_deeper']:
        # if you want all time rankings
        all_time = st.checkbox('**Show All Time Ranks**', value=True, key=f'all_time')
        if st.session_state['all_time'] == False:
            # if no all time rankings, add a season select box
            season = st.selectbox('**Select the Season**', season_list, key=f'season')
        if st.session_state['explanations'] and st.session_state['all_time']:
                st.write(f'''
                        **Choose a stat to see where the player ranks in the league \*All Time.**\n
                        ''')
                st.caption('''
                        **\*Ranks calculated for data back to the 1996-97 season.**\n
                        ''')

        # if you want to filter by games played
        check_gp = st.checkbox('**:green[Games Played] Filter**', value=False, key=f'check_gp')
        if st.session_state['check_gp']:
            gp = st.slider('Number of games played', 0, 82, 65, key=f'gp')
            years_in_league = None
            check_years = st.checkbox('**:green[Years Minimum] Filter**', value=True, key=f'check_years')

            # optional additional filter for # of years in the league
            if st.session_state['check_years']:
                max_years = all_player_years['YEARS_IN_LEAGUE'].max()
                # max years in league
                years_in_league = st.slider('Minimum years in league', 0, max_years, 5)
                # get the players who have played at least years_in_league seasons
                player_years = all_player_years[all_player_years['YEARS_IN_LEAGUE'] >= years_in_league]

            # rerun the ranking with the new gp and years in league filters
            season_rank_list = get_season_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp)
            tmp_all_rank_list = get_all_time_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp, years_in_league)

            # if all time rankings are selected, merge the dataframes together
            if st.session_state['all_time']:
                tmp_all_rank_list_df = merge_rank_dfs(tmp_all_rank_list)
                # if empty the filters have no players
                if tmp_all_rank_list_df.empty:
                    st.warning(f'No players played >= :green[{gp}] games in >= :green[{years_in_league}] seasons! Ranks below are for all players without filters applied.')
                    reset = True # variable to reset the filters to all time rankings; doesn't actually reset, but flag that results in the original filters being used
                # if the filters have players, get the year count for how many years they fit the filters
                else:
                    all_rank_list_df = tmp_all_rank_list_df.copy()
                    year_counts = all_rank_list_df[['PLAYER_NAME', 'YEARS_COUNT']].copy()
                rank_df = all_rank_list_df
            # else, use the season rank list
            else:
                season_rank_df = join_season_dfs(season_rank_list)
                rank_df = season_rank_df
                season_players_df = player_years[player_years['YEAR'] == season].copy()
                rank_df = rank_df[rank_df['YEAR'] == season]
                # keep only the players in the rank_df
                season_players_df = season_players_df[season_players_df['PLAYER_NAME'].isin(rank_df['PLAYER_NAME'])].copy()
                player_years = player_years[player_years['YEAR'] == season]
                # keep only the players in the season_players_df
                rank_df = rank_df[rank_df['PLAYER_NAME'].isin(season_players_df['PLAYER_NAME'])].copy()
        else:
            rank_df = all_rank_list_df.copy()
    else:
        # get the current season data
        rank_df = season_avg_df
        # add the years in league column to the dataframe
        rank_df = rank_df[rank_df['YEAR'] == season]

    # SETUP THE STAT DROPDOWN AND BUTTON
    left, right = st.columns(2, vertical_alignment='bottom')
    with right:
        if st.button('**Random Stat**', key=f'random_stat'):
            # get a random stat
            stat_index = random.randint(0, len(stat_list)-1)
            stat = stat_list[stat_index]
            st.session_state['stat'] = stat 
    with left:
        stat = st.selectbox('**Select a Stat**', stat_list, index=1, placeholder='Stat Name...', key=f'stat')
    # keep only the rank column
    rank, percentile = f'{stat}_Rank', f'{stat}_Percentile'
    # check if the first rank is 1
    if rank_df[rank].min() != 1:
        # rerank the data in the rank column to make sure it start at 1
        rank_df[rank] = rank_df[rank].rank(method='first', ascending=True)
    # get a list of the number of ranks in the league
    rank_list = sorted(rank_df[rank].unique(), reverse=False)
    # convert the rank list to a list of int
    rank_list = [int(rank) for rank in rank_list if str(rank) != 'nan']

    # SETUP THE RANK DROPDOWN AND BUTTON
    left_rank, right_rank = st.columns(2, vertical_alignment='bottom')
    with right_rank:
        if st.button('**Random Rank**', key=f'random_rank'):
            # get a random rank
            rank_index = random.randint(0, len(rank_list)-1)
            rank_num = rank_list[rank_index]
            st.session_state['rank'] = rank_num
    with left_rank:
        rank_num = st.selectbox('**Select a Rank**', rank_list, index=0, placeholder='Rank...', key=f'rank')
    # get the x ranked player
    player = rank_df[rank_df[rank] == rank_num]['PLAYER_NAME'].values[0]
    player_emoji = annotate_with_emojis(player, emoji_df)
    # get the actual stat value for the player
    stat_value = rank_df[rank_df['PLAYER_NAME'] == player][stat].values[0]
    years_in_league = all_player_years[all_player_years['PLAYER_NAME'] == player]['YEARS_IN_LEAGUE'].values[0]
    # add the values to the df 
    tmp_df = pd.DataFrame({'PLAYER_NAME': [player], 'RANK': [rank_num], 'STAT': [stat], 'VALUE': [stat_value], 'SEASON': [season], 'YEARS': [years_in_league]})
    st.divider()
    if st.session_state['go_deeper']:
        if st.session_state['all_time']:
            if st.session_state['check_gp'] and reset == False:
                # the count ofthe years the player matched the given search filters
                year_count = year_counts[year_counts['PLAYER_NAME'] == player]['YEARS_COUNT'].values[0]
                st.write(f'In the :green[**{year_count}**] seasons where **{player_emoji}** played at least :green[{gp} games], he averaged :green[**{round(stat_value,2)}**  **{stat}**] good for :violet[**#{rank_num}**] All Time.')
            else:
                st.write(f'**{player_emoji}** averaged :green[**{round(stat_value,2)}**  **{stat}**], which is :violet[**#{rank_num}**] **All Time**.')
        else:
            st.write(f'**{player_emoji}** averaged :green[**{round(stat_value,2)}**  **{stat}**], which is :violet[**#{rank_num}**] in the :grey[**{season} season**].')
    else:
        st.write(f'**{player_emoji}** averaged :green[**{round(stat_value,2)}**  **{stat}**], which is :violet[**#{rank_num}**] in the :grey[**{season} season**].')
    st.expander(f'**{stat} {season} Data**', expanded=False)
    with st.expander(f':green[**{stat} {season} Data**]', expanded=False):
        cols = ['PLAYER_NAME', 'TEAM_ABBREVIATION', rank, stat, 'YEARS_IN_LEAGUE']
        # add years in league to the dataframe
        all_player_years = all_player_years.drop_duplicates(subset=['PLAYER_NAME'], keep='last')
        # set the years in league to take values from the player years dataframe
        rank_df = pd.merge(rank_df, all_player_years, on=['PLAYER_NAME'], how='left')
        rank_df = rank_df[cols]
        output_df = rank_df
        #output_df = pd.merge(data_df, rank_df, on=['PLAYER_NAME', 'TEAM_ABBREVIATION'])
        output_df = output_df.sort_values(by=rank, ascending=True).reset_index(drop=True)
        st.dataframe(output_df, use_container_width=True, hide_index=True)

# TODO: if possible, make this like queereable where it shows up to the last x searches (like a search history)
# TODO: add secret emojis here (really hard ones to find; need to do x searches, hit certain buttons, etc.)


