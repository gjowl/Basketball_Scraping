import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import change_to_team_colors, plot_quadrant_scatter, get_player_data, get_player_ranks, create_player_rank_bar_graph, set_axis_text, adjust_axis, make_year_scatterplot

# SET PAGE CONFIG
st.set_page_config(page_title='Player Search',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Player Search')

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

# MAIN
## PAGE SETUP BELOW
'''
 - Select a player from the dropdown
 - Tabs for Traditional, Shooting, and Non-Shooting stats
 - Graphs and rankings for the player
 - Button to show player data
'''
## TODO: clean this code up
## TODO: add a blurb about the page and what it does
# TODO: get a average for all years for each stat and plot as another line; gives context to the player being an outlier or not

# FUNCTIONS
## traverse directory to load data
def create_year_data_dict(datadir):
    year_data_dict = {}
    for root, dirs, files in os.walk(datadir):
        for file in files:
            # look if the name of the file is what you want
            # read in the file
            tmp_df = pd.read_csv(os.path.join(root, file))
            # get the filename and remove the extension, separate by _
            filename = file.split('_')[0]
            # check if ~ is in the filename, if so don't add it to the dictionary
            if '~' in filename:
                continue
            # add the df to the dictionary with the filename as the key
            year_data_dict[filename] = tmp_df
    return year_data_dict

year_data_dict = create_year_data_dict(datadir)

## get all the unique player names from the year_data_dict
player_names = pd.Series()
for key in year_data_dict.keys():
    player_names = pd.concat([player_names, year_data_dict[key]['PLAYER_NAME']])
player_names = player_names.unique()

## create a search bar for the player names
player = st.selectbox('*Select the player to load*', player_names)

## get the data for the player from all years they played in the league
player_df = get_player_data(year_data_dict, player)

# change the YEAR column to be SEASON, keep the split by _
player_df['SEASON'] = player_df['YEAR'].str.split('-').str[0]

## variables for the stats to get
name_and_year = ['PLAYER_NAME', 'YEAR']
cols_to_keep = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MPG'] # keep the player name, team abbreviation, and GP
percent = ['FG%', '2P%', '3P%']
#shots = ['FG%', 'FGA_PG', 'FGM_PG', '2P%', '2PA_PG', '2PM_PG', '3P%', '3PA_PG', '3PM_PG', 'FT%', 'FTA_PG', 'FTM_PG'] # make into quadrant plots
shots_types = [['FG%', 'FGA_PG', 'FGM_PG'], ['2P%', '2PA_PG', '2PM_PG'], ['3P%', '3PA_PG', '3PM_PG'], ['FT%', 'FTA_PG', 'FTM_PG']] # make into quadrant plots
shot_pairs = [['FGA_PG', 'FGM_PG'], ['2PA_PG', '2PM_PG'], ['3PA_PG', '3PM_PG'], ['FTA_PG', 'FTM_PG']]
traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'TOV_PG', 'PF_PG'] # unsure yet
traditional_groups = [['MPG', 'PPG', 'APG'], ['RPG', 'SPG', 'BPG'], ['AST_TO', 'TOV_PG', 'PF_PG']] # unsure yet
quadrant_pairs = [['PPG', 'APG'], ['APG', 'TOV_PG'], ['RPG', 'BPG'], ['OREB_PG', 'DREB_PG'], ['SPG', 'PF_PG']] # make into quadrant plots
advanced = ['AST_TO', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%']

## get the dataframes for the player
percent_df = player_df[name_and_year + percent]
#shots_df = player_df[name_and_year + shots]
traditional_df = player_df[name_and_year + traditional]

## TABS 
tab1, tab2, tab3, tab4 = st.tabs(['**Traditional**', '**Shooting**', '**Non-Shooting**', '**Advanced**']) # add in advanced as well
n = 0
with tab1:
    st.header('Traditional Boxscore Stats')
    st.dataframe(traditional_df, use_container_width=True, hide_index=True)
    # add a dropdown to select the season of interest
    season = st.selectbox('Select the season of interest', player_df['YEAR'].unique())
    # get the stats for the season
    season_df = year_data_dict[season]
    if st.toggle('**GP Threshold**'):
        # add in a slider for the number of games played
        gp = st.slider('Number of games played', 0, 82, 10)
        # filter the dataframe to only include players with more than 10 games played
        season_df = season_df[season_df['GP'] > gp]
    # get the player rankings for the player in the season
    player_ranks = get_player_ranks(season_df, player, traditional)
    create_player_rank_bar_graph(season_df, player_ranks, player, team_colors)
    
    if st.button('Show Ranked Data'):
        # keep the ranked columns
        st.write(f'Below are the ranked stats for the {season} season')
        rank_cols = [col for col in season_df.columns if 'Rank' in col]
        season_df = season_df[cols_to_keep + rank_cols]
        st.dataframe(season_df, use_container_width=True, hide_index=True)
        st.button('Hide Ranked Data')
    # get the top ranks for the player
    player_ranks = player_ranks.sort_values(by='Rank', ascending=True)
    # check if any ranks are within the top 100
    if st.toggle('**Show All Ranked Plots**'):
        for pair in quadrant_pairs:
            plot_quadrant_scatter(season_df, pair[0], pair[1], player_df, team_colors)
    else:
        if player_ranks['Rank'].min() < 100:
            # going to use specialized rankings for the player
            # get the top rank category
            top_rank = player_ranks['Rank'].idxmin()
            # TODO: it might be time to start pulling in the advanced stats for players
            pairs = []
            # check if the top rank is in the list of ranks
            if top_rank is 'PPG' or top_rank is 'APG':
                # use PPG vs APG, RPG vs BPG, SPG vs MPG
                pairs = [['PPG', 'APG'], ['APG', 'TOV_PG'], ['SPG', 'MPG']]
            elif top_rank is 'RPG':
                # use RPG vs BPG, RPG vs MPG, PPG vs RPG
                pairs = [['RPG', 'BPG'], ['RPG', 'MPG'], ['PPG', 'RPG']]
            elif top_rank is 'SPG':
                # use SPG vs MPG, PPG vs SPG, APG vs SPG
                pairs = [['SPG', 'MPG'], ['PPG', 'SPG'], ['APG', 'SPG']]
            else:
                # going to just use generic rankings: [PPG vs APG, SPG vs MPG, RPG vs BPG]
                pairs = [['PPG', 'APG'], ['SPG', 'MPG'], ['RPG', 'BPG']]
            for pair in pairs:
                plot_quadrant_scatter(season_df, pair[0], pair[1], player_df, team_colors)
with tab2:
    st.header(f'{player} Shooting Stats Trajectory by Year')
    # TODO: show the boxscore data for the player
    if st.button('Show Shooting Data'):
        st.write('Below are the shooting stats for the player')
        st.dataframe(player_df, use_container_width=True, hide_index=True)
        st.button('Hide Shooting Data')
    # add a toggle to add a line to the plot for the average of the stat
    show_lines = False
    if st.toggle('**Add lines by year**', key='lines_by_year'):
        show_lines = True
    for shots in shots_types:
        figs = []
        for shot in shots:
            fig = make_year_scatterplot(player_df, shot, team_colors, show_lines)
            figs.append(fig)
            n+=1
        c1, c2, c3 = st.columns(3)
        with c1:
            st.plotly_chart(figs[0], key=n, use_container_width=True)
            n+=1
        with c2:
            st.plotly_chart(figs[1], key=n, use_container_width=True)
            n+=1
        with c3:
            st.plotly_chart(figs[2], key=n, use_container_width=True)
            n+=1
with tab3:
    st.header('Non-Shooting Stats Trajectory by Year')
    # TODO: show the boxscore data for the player
    if st.button('Show Non-Shooting Data', key='nonshooting'):
        st.write('Below are the non-shooting stats for the player')
        st.dataframe(player_df, use_container_width=True, hide_index=True)
        st.button('Hide Non-Shooting Data', key='hide_nonshooting')
    show_lines = False
    if st.toggle('Add lines by year', key='line-nonshooting'):
        show_lines = True
    for group in traditional_groups:
        figs = []
        for stat in group:
            fig = make_year_scatterplot(player_df, stat, team_colors, show_lines)
            figs.append(fig)
            n+=1
        c1, c2, c3 = st.columns(3)
        with c1:
            st.plotly_chart(figs[0], key=n, use_container_width=True)
            n+=1
        with c2:
            st.plotly_chart(figs[1], key=n, use_container_width=True)
            n+=1
        with c3:
            st.plotly_chart(figs[2], key=n, use_container_width=True)
            n+=1
        # TODO: show the legend on the right side of the plots
with tab4:
    datadir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD/ADVANCED'
    advanced_data_dict = create_year_data_dict(datadir)
    ## get the data for the player from all years they played in the league
    player_df = get_player_data(advanced_data_dict, player)

    # change the YEAR column to be SEASON, keep the split by _
    player_df['SEASON'] = player_df['YEAR'].str.split('-').str[0]

    # read in the advanced stats data
    stats = ['W%', 'TS%', 'USG%', 'AST%', 'OREB%', 'DREB%', 'REB%', 'POSS_PG', 'EFG%']
    for stat in stats:
        fig = make_year_scatterplot(player_df, stat, team_colors, show_lines)
        st.plotly_chart(fig, use_container_width=True)
    ranks = ['OFF_RATING_RANK', 'DEF_RATING_RANK', 'AST%_RANK', 'AST_TO_RATIO_RANK', 'AST_PCT_RANK', 'STL_PCT_RANK', 'BLK_PCT_RANK', 'OREB%_RANK', 'DREB%_RANK', 'REB%_RANK', 'TS%_RANK', 'USG%_RANK', 'EFG%_RANK']


if st.button(f'Show All {player} Data'):
    # show all the data with no scroll bar
    st.dataframe(player_df, use_container_width=True, hide_index=True)
    st.button('Hide Data', key=f'hide_{player}_data')
# an interesting alternate idea (or maybe concurrent) is to basically make the website a scrolling timeline of the player: Kind of like the spotify wrapped, but a timeline of the player with 
# their most important stats and their overall impact on the game? Would some sort of impact on the game metric be interesting? How would I define that just using stats?
# I think I have to start with the most impactful players: Steph is an outlier in 3pt shooting all time. But whenever it started (so he has a large difference in 3PAs to how quickly it gets closer)
# could look at something like that? As if the player is a trendsetter if they are an outlier in a stat and the rest of the league (or at least a certain number of players follows suit?)
