import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import emoji_check, annotate_with_emojis, create_player_rank_bar_graph, create_year_data_dict

# SET PAGE CONFIG
st.set_page_config(page_title='Player Rankings',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('🔍 Player Rankings')

# VARIABLES 
#cwd = os.getcwd()
#data = pd.read_csv(f'{cwd}/example_data.csv')
#datadir = 'H:/NBA_API_DATA/BOXSCORES/2024-12-12'
#datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'
#contains = 'all_game' # file you want to read
datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD'
advancedDir = '/mnt/h/NBA_API_DATA/BOXSCORES/ADVANCED'
contains = '2023-24_boxscore' # file you want to read
colors = '/mnt/d/github/Basketball_Scraping/site/team_colors_hex.csv'
options = '/mnt/d/github/Basketball_Scraping/site/options.csv'
emoji_file = '/mnt/d/github/Basketball_Scraping/site/emoji_players.csv'
go_deeper = False
all_time = True
season = '2024-25'
start_player = 'LeBron James'

# 
cols = st.columns(2)
with cols[0]:
    go_deeper = st.checkbox('**:grey[Go Deeper]**', value=True)
with cols[1]:
    explanation = st.checkbox('**:grey[Explanations]**', value=True)

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

def get_season_player_rankings(_year_data_dict, _advanced_data_dict, _rank_cols, _check_gp, _gp):
    all_ranks, output_dfs = [], []
    for ranks in _rank_cols:
        # get the player rankings for the season
        tmp_df, tmp_out_df = pd.DataFrame(), pd.DataFrame()
        for key in _year_data_dict.keys():
            season_df = _year_data_dict[key]
            # remove data for players with less than games played
            if 'TS%' in ranks:
                season_df = _advanced_data_dict[key]
            #if _check_gp:
            #    season_df = season_df[season_df['GP'] >= _gp]
            #    # get the player rankings for the season
            #    player_ranks = get_ranks(season_df, ranks)
            #    tmp_df = pd.concat([tmp_df, player_ranks], ignore_index=True)
            #    tmp_out_df = pd.concat([tmp_out_df, season_df], ignore_index=True)
            #else:
            player_ranks = get_ranks(season_df, ranks)
            tmp_df = pd.concat([tmp_df, player_ranks], ignore_index=True)
            tmp_out_df = pd.concat([tmp_out_df, season_df], ignore_index=True)
        output_dfs.append(tmp_out_df) 
        all_ranks.append(tmp_df)
    return all_ranks, output_dfs

def get_all_time_player_rankings(_year_data_dict, _advanced_data_dict, _rank_cols, _check_gp, _gp):
    all_ranks, output_dfs = [], []
    for ranks in _rank_cols:
        # get the player rankings for the season
        tmp_df = pd.DataFrame()
        for key in _year_data_dict.keys():
            season_df = _year_data_dict[key]
            if 'TS%' in ranks:
                season_df = _advanced_data_dict[key]
            # remove data for players with less than games played
            #if _check_gp:
            #    season_df = season_df[season_df['GP'] >= _gp]
            tmp_df = pd.concat([tmp_df, season_df], ignore_index=True)
        # get the mean for each stat in the rank list
        avg_df = tmp_df.groupby('PLAYER_NAME')[ranks].mean().reset_index()
        # append the first team abbreviation to the dataframe
        avg_df['TEAM_ABBREVIATION'] = tmp_df.groupby('PLAYER_NAME')['TEAM_ABBREVIATION'].first().values
        tmp_ranks = get_ranks(avg_df, ranks, _season=False)
        #st.dataframe(tmp_ranks, use_container_width=True, hide_index=True)
        all_ranks.append(tmp_ranks)
        output_dfs.append(avg_df)
    return all_ranks, output_dfs

def transform_ranks_for_plotting(_df):
    # separate by _ into index and stat
    ranks, percentiles = _df.columns[_df.columns.str.contains('_Rank')].tolist(), _df.columns[_df.columns.str.contains('_Percentile')].tolist() 
    # separate ranks by _
    ranks, percentiles = [rank.split('_Rank')[0] for rank in ranks], [percentile.split('_Percentile')[0] for percentile in percentiles]
    player_ranks = pd.DataFrame()
    for stat in ranks:
        player_ranks[stat] = [_df[f'{stat}_Percentile'].values[0], _df[f'{stat}_Rank'].values[0]]
    player_ranks = player_ranks.T
    player_ranks.columns = ['Percentile', 'Rank']
    return player_ranks

def merge_rank_dfs(_dfs):
    output_df = pd.DataFrame()
    for df in _dfs:
        if output_df.empty:
            output_df = df.copy()
        else:
            output_df = pd.merge(output_df, df, on=['PLAYER_NAME', 'TEAM_ABBREVIATION'])
    return output_df

# MAIN
## PAGE SETUP BELOW
## SELECT A PLAYER FROM THE DROPDOWN
## TABS SEPARATED STATS AND GRAPHS
## BUTTON TO SHOW PLAYER DATA

# LOAD IN THE DATA
year_data_dict, advanced_data_dict = create_year_data_dict(datadir), create_year_data_dict(advancedDir)
## get all the unique player names from the year_data_dict
player_names = pd.Series()
for key in year_data_dict.keys():
    player_names = pd.concat([player_names, year_data_dict[key]['PLAYER_NAME']])
player_names = player_names.unique()

# TOGGLE FOR GP THRESHOLD

st.write('**Toggle to filter by :green[Games Played]**')
if st.toggle('**GP Threshold**'):
    # add in a slider for the number of games played
    gp = st.slider('Number of games played', 0, 82, 65)
    check_gp = True
# GET RANKINGS FOR ALL PLAYERS
all_ranks, all_avgs = get_season_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp)
all_time_ranks, all_time_avgs = get_all_time_player_rankings(year_data_dict, advanced_data_dict, rank_cols, check_gp, gp)


## TABS START HERE
tabs = st.tabs(['**Player Search**', '**Rank Finder**'])

# TAB 1: PLAYER SEARCH
with tabs[0]:
    if explanation: 
        if go_deeper == False:
            st.write('''
                    ***Where did Austin Reaves rank in PPG in the current season?***\n
                    **Below you can choose a player and see their rank in all stats.**\n
                    ''')
        else:
            st.write('''
                    ***Where did xxx rank in PPG in a given season?***\n
                    **Choose a player and season below to see their ranks in the given season. \*All Time Ranks are included at the bottom of the page.**\n
                    ''')
            st.caption('''
                    **\*Ranks calculated for data back to the 1996-97 season.**\n
                    ''')
    ## SELECT A PLAYER FROM THE DROPDOWN
    # make a selectbox for the player names, index at the start_player
    player = st.selectbox('**Select a Player to Load Rank Graphs**', player_names, index=player_names.tolist().index(start_player), placeholder='Player Name...')
    player_emoji = annotate_with_emojis(player, emoji_df)
    ## get the data for the player from all years they played in the league
    player_dfs, player_avg_dfs = [], []
    for df, avg_df in zip(all_ranks, all_avgs):
        player_df = df[df['PLAYER_NAME'] == player].reset_index(drop=True)
        player_avg = avg_df[avg_df['PLAYER_NAME'] == player].reset_index(drop=True)
        player_dfs.append(player_df)
        player_avg_dfs.append(player_avg)
    titles = ['Traditional', 'Shooting', 'Advanced']
    # reverse the list to get the most recent season first
    season_list = sorted(player_dfs[0]['YEAR'].unique(), reverse=True) 
    if go_deeper == False:
        season = st.selectbox('**Select the Season**', season_list, key=f'season_{plot_number}')
    st.divider()
    st.write(f'**{player_emoji} {season} Season Ranks**')
    for ranks,df,avg_df,title in zip(rank_cols, player_dfs, player_avg_dfs, titles):
        st.expander(f'**{title}**', expanded=False)
        with st.expander(f':green[**{title}**]', expanded=False):
            player_df = df[df['PLAYER_NAME'] == player].reset_index(drop=True)
            season_df = player_df[player_df['YEAR'] == season].reset_index(drop=True)
            player_gp = player_df['GP'].max()
            if gp > player_gp:
                st.warning(f'{player_emoji} has only played {player_gp} games this season. Please select a lower number of games played.')
                st.stop()
            player_ranks = transform_ranks_for_plotting(season_df) 
            fig = create_player_rank_bar_graph(season_df, player_ranks, player, title, team_colors) 
            # setup the hover template with the avg_df values
            st.plotly_chart(fig, use_container_width=True, key=f'player_rank_bar_graph_{plot_number}')
            # show the player data in a table
            season_avg_df = avg_df[avg_df['YEAR'] == season].reset_index(drop=True)
            season_avg_df = season_avg_df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP'] + ranks]
            season_avg_df[ranks] = season_avg_df[ranks].round(2)
            plot_number += 1
    if go_deeper == False:
        st.divider()
        st.write(f'**{player_emoji} All Time Ranks**')
        st.expander('**All Time**', expanded=False)
        with st.expander(':rainbow[**All Time**]', expanded=False):
            for df,avg_df,title in zip(all_time_ranks,all_time_avgs,titles):
                player_df = df[df['PLAYER_NAME'] == player].reset_index(drop=True)
                player_ranks = transform_ranks_for_plotting(player_df) 
                fig = create_player_rank_bar_graph(player_df, player_ranks, player, title, team_colors) 
                st.plotly_chart(fig, use_container_width=True, key=f'player_rank_bar_graph_{plot_number}')
                player_avg_df = avg_df[avg_df['PLAYER_NAME'] == player].reset_index(drop=True)
                # remove _Percentile and _Rank from the columns
                player_avg_df = player_avg_df[[col for col in player_avg_df.columns if '_Percentile' not in col and '_Rank' not in col]]
                # round all but player name and team abbreviation to 2 decimal places
                cols = player_avg_df.columns.tolist()
                cols = [col for col in cols if col not in ['PLAYER_NAME', 'TEAM_ABBREVIATION']]
                player_avg_df[cols] = player_avg_df[cols].round(2)
                plot_number += 1
# TAB 2: STAT SEARCH
## SELECT A STAT TO PLOT
# TODO: fix the seasonal rank search at some point; the merge here doesn't work because of same cols with diff values
#season_ranks_df = merge_rank_dfs(all_ranksj
#season_avgs_df = merge_rank_dfs(all_avgs)
season_ranks_df, season_avg_df = pd.DataFrame(), pd.DataFrame()
cols = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'YEAR', 'SEASON']
cols_data = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'YEAR', 'SEASON', 'AGE', 'MPG', 'clock', 'FG%', 'FT%', '3P%', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'STOCKS_PG', 'TOV_PG', 'PF_PG', 'AST_TO']
for df, avg_df in zip(all_ranks, all_avgs):
    if season_ranks_df.empty:
        season_ranks_df = df.copy()
        season_avg_df = avg_df.copy()
    else:
        season_ranks_df.set_index(cols, inplace=True)
        season_avg_df.set_index(cols, inplace=True)
        tmp_df = df.copy()
        tmp_avg_df = avg_df.copy()
        tmp_df.set_index(cols, inplace=True)
        tmp_avg_df.set_index(cols, inplace=True)
        season_ranks_df = season_ranks_df.join(tmp_df, lsuffix='_tmp', rsuffix='_tmp_2', how='outer').reset_index()
        season_avg_df = season_avg_df.join(tmp_avg_df, lsuffix='_tmp', rsuffix='_tmp_2', how='outer').reset_index()
# remove the _tmp and _tmp_2 columns from the dataframe
season_avg_df = season_avg_df.loc[:, ~season_avg_df.columns.str.contains('_tmp_2')]
# remove anything with rank or percentile in the name
season_avg_df = season_avg_df.loc[:, ~season_avg_df.columns.str.contains('_RANK|_Rank|_Percentile')]
# remove the AGE_tmp column
season_avg_df = season_avg_df.loc[:, ~season_avg_df.columns.str.contains('AGE_tmp|MPG_tmp|FG%_tmp|FGM_PG_tmp|FGA_PG_tmp|AST_TO_tmp')]
# rename the columns to remove the _tmp and _tmp_2 suffixes
season_avg_df.columns = [col.split('_tmp')[0] for col in season_avg_df.columns]
all_time_ranks_df = merge_rank_dfs(all_time_ranks)
all_time_avgs_df = merge_rank_dfs(all_time_avgs)


with tabs[1]:
    if explanation:
        if go_deeper == False:
            st.write('''
                    **Choose a stat to see where the player ranks in the league this season.**\n
                    ''')
    all_rank_cols = pd.concat(all_ranks, ignore_index=True)
    stat_list = all_rank_cols.columns[all_rank_cols.columns.str.contains('_Rank')].tolist()
    # remove rank from the stat list
    stat_list = [stat.split('_Rank')[0] for stat in stat_list]
    stat = st.selectbox('**Select a Stat**', stat_list, index=1, placeholder='Stat Name...')
    if go_deeper:
        all_time = st.checkbox('**Show All Time Ranks**', value=True)
        if explanation and all_time:
                st.write(f'''
                        **Choose a stat to see where the player ranks in the league \*All Time.**\n
                        ''')
                st.caption('''
                        **\*Ranks calculated for data back to the 1996-97 season.**\n
                        ''')
        if all_time == False:
            season = st.selectbox('**Select the Season**', season_list, key=f'season_{plot_number}')
            rank_df = season_ranks_df
            rank_df = rank_df[rank_df['YEAR'] == season]
            data_df = season_avg_df
            data_df = data_df[data_df['YEAR'] == season]
        else:
            rank_df = all_time_ranks_df
            data_df = all_time_avgs_df
    else:
        # get the current season data
        rank_df = season_ranks_df
        rank_df = rank_df[rank_df['YEAR'] == season]
        data_df = season_avg_df
        data_df = data_df[data_df['YEAR'] == season]
    # keep only the rank column
    rank, percentile = f'{stat}_Rank', f'{stat}_Percentile'
    rank_df = rank_df[['PLAYER_NAME', 'TEAM_ABBREVIATION', rank, percentile]]
    # if the value in the stat is not unique, make it unique
    # get a list of the number of ranks in the league
    rank_list = sorted(rank_df[rank].unique(), reverse=False)
    # convert the rank list to a list of int
    rank_list = [int(rank) for rank in rank_list if str(rank) != 'nan']
    rank_num = st.selectbox('**Select a Rank**', rank_list, index=0, placeholder='Rank...')
    # get the x ranked player
    player = rank_df[rank_df[rank] == rank_num]['PLAYER_NAME'].values[0]
    player_emoji = annotate_with_emojis(player, emoji_df)
    # get the actual stat value for the player
    stat_value = data_df[data_df['PLAYER_NAME'] == player][stat].values[0]
    # add the values to the df 
    tmp_df = pd.DataFrame({'PLAYER_NAME': [player], 'RANK': [rank_num], 'STAT': [stat], 'VALUE': [stat_value], 'SEASON': [season]})
    if go_deeper:
        if all_time and check_gp == False:
            st.write(f'**{player_emoji}** averaged :green[**{round(stat_value,2)}**  **{stat}**], which is :violet[**#{rank_num}**] **All Time**.')
    if check_gp:
        if gp < 65:
            st.write(f'In the seasons where **{player_emoji}** played at least :gray[{gp} games], he averaged :green[**{round(stat_value,2)}**  **{stat}**] good for :violet[**#{rank_num}**] All Time.')
        else:
            st.write(f'In the seasons where **{player_emoji}** played at least :green[{gp} games], he averaged :green[**{round(stat_value,2)}**  **{stat}**] good for :violet[**#{rank_num}**] All Time.')
    else:
        st.write(f'**{player_emoji}** averaged :green[**{round(stat_value,2)}**  **{stat}**], which is :violet[**#{rank_num}**] in the :grey[**{season} season**].')
    st.expander(f'**{stat} {season} Data**', expanded=False)
    with st.expander(f':green[**{stat} {season} Data**]', expanded=False):
        cols = ['PLAYER_NAME', 'TEAM_ABBREVIATION', rank]
        cols_data = ['PLAYER_NAME', 'TEAM_ABBREVIATION', stat]
        data_df = data_df[cols_data]
        rank_df = rank_df[cols]
        output_df = pd.merge(data_df, rank_df, on=['PLAYER_NAME', 'TEAM_ABBREVIATION'])
        output_df = output_df.sort_values(by=rank, ascending=True).reset_index(drop=True)
        st.dataframe(output_df, use_container_width=True, hide_index=True)
    # TODO: if possible, make this like queereable where it shows up to the last x searches (like a search history)

#if st.button(f'Show All {player} Data'):
#    # show all the data with no scroll bar
#    player_df = get_player_data(year_data_dict, player)
#    st.dataframe(player_df, use_container_width=True, hide_index=True)
#    st.button('Hide Data', key=f'hide_{player}_data')
# an interesting alternate idea (or maybe concurrent) is to basically make the website a scrolling timeline of the player: Kind of like the spotify wrapped, but a timeline of the player with 
# their most important stats and their overall impact on the game? Would some sort of impact on the game metric be interesting? How would I define that just using stats?
# I think I have to start with the most impactful players: Steph is an outlier in 3pt shooting all time. But whenever it started (so he has a large difference in 3PAs to how quickly it gets closer)
# could look at something like that? As if the player is a trendsetter if they are an outlier in a stat and the rest of the league (or at least a certain number of players follows suit?)
