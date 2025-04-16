import streamlit as st
import os, pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import plotly.graph_objects as go
from functions import change_to_team_colors, plot_quadrant_scatter, get_player_data, get_player_ranks, create_player_rank_bar_graph, set_axis_text, adjust_axes

# SET PAGE CONFIG
st.set_page_config(page_title='Stat Search',
                   page_icon='🔍',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Welcome to the stat search page!')

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


## traverse directory to load data
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

## get all the unique player names from the year_data_dict
player_names = pd.Series()
for key in year_data_dict.keys():
    player_names = pd.concat([player_names, year_data_dict[key]['PLAYER_NAME']])
player_names = player_names.unique()

## create a search bar for the player names
player = st.selectbox('Select the player to load', player_names)

## get the data for the player from all years they played in the league
player_df = get_player_data(year_data_dict, player)
if st.button('Show Data'):
    # show all the data with no scroll bar
    st.dataframe(player_df, use_container_width=True, hide_index=True)
    st.button('Hide Data')

## variables for the stats to get
name_and_year = ['PLAYER_NAME', 'YEAR']
cols_to_keep = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MPG'] # keep the player name, team abbreviation, and GP
percent = ['FG%', '2P%', '3P%']
shots = ['FG%', 'FGA_PG', 'FGM_PG', '2P%', '2PA_PG', '2PM_PG', '3P%', '3PA_PG', '3PM_PG', 'FT%', 'FTA_PG', 'FTM_PG'] # make into quadrant plots
shot_pairs = [['FGA_PG', 'FGM_PG'], ['2PA_PG', '2PM_PG'], ['3PA_PG', '3PM_PG'], ['FTA_PG', 'FTM_PG']]
traditional = ['MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'OREB_PG', 'DREB_PG', 'TOV_PG', 'PF_PG'] # unsure yet
quadrant_pairs = [['PPG', 'APG'], ['APG', 'TOV_PG'], ['RPG', 'BPG'], ['OREB_PG', 'DREB_PG'], ['SPG', 'PF_PG']] # make into quadrant plots
#advanced = ['AST_TO', 'NBA_FANTASY_PTS_PG', 'TS%', 'USG%', 'OREB%', 'DREB%', 'AST%', 'STL%', 'BLK%']

## get the dataframes for the player
percent_df = player_df[name_and_year + percent]
shots_df = player_df[name_and_year + shots]
traditional_df = player_df[name_and_year + traditional]

## TABS 
tab1, tab2, tab3 = st.tabs(['Traditional', 'Percent', 'Shooting'])
with tab1:
    st.header('Traditional Stats')
    st.write('Below are the traditional stats for the player')
    st.dataframe(traditional_df, use_container_width=True, hide_index=True)
    # add a dropdown to select the season of interest
    season = st.selectbox('Select the season of interest', player_df['YEAR'].unique())
    # get the stats for the season
    season_df = year_data_dict[season]
    if st.toggle('GP Threshold'):
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
    if st.toggle('Show All Ranked Plots'):
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
    st.header('Percent Stats')
    if st.button('Show Percent Data'):
        st.write('Below are the shooting percentages for the player')
        st.dataframe(percent_df, use_container_width=True, hide_index=True)
        st.button('Hide Percent Data')
    fig_list = []
    # plot a box plot with the points overlaid for each stat
    fig = go.Figure()
    for stat in percent:
        # make a array of the stat with the same size as the percent_df
        x = [stat] * len(percent_df[stat])
        # create a hover label with the year and the stat value
        hover_label = [f'{year}: {value}' for year, value in zip(percent_df['YEAR'], percent_df[stat])]
        fig.add_trace(go.Box(y=percent_df[stat], x=x, name=stat, boxmean='sd', line_color='#F27522', marker_color='orange', hoverinfo='text', hovertext=hover_label, boxpoints='all', pointpos=0, opacity=0.5, showlegend=False))
        # replace the hover label w/ the {YEAR}: {percentage} to the points
        fig.update_traces(marker=dict(size=7, color='white', line=dict(width=3, color='white')))
        set_axis_text(fig)
    st.plotly_chart(fig, use_container_width=True)
with tab3:
    st.header(f'{player} Shooting Stats')
    if st.button('Show Shooting Data'):
        st.write('Below are the shooting stats for the player')
        st.dataframe(shots_df, use_container_width=True, hide_index=True)
        st.button('Hide Shooting Data')
    # add a toggle to add a line to the plot for the average of the stat
    show_lines = False
    if st.toggle('Add lines by year', key='line'):
        show_lines = True
    figs = []
    for shot_pair in shot_pairs:
        x_axis, y_axis = shot_pair[1], shot_pair[0]
        fig = px.scatter(player_df, x=x_axis, y=y_axis, color='YEAR', hover_name='TEAM_ABBREVIATION', title=f'{x_axis} vs {y_axis}')
        fig.update_traces(marker=dict(size=10, line=dict(width=2, color='black')))
        fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis)
        if show_lines:
            # draw a line between consecutive year points
            fig.add_trace(go.Scatter(x=player_df[x_axis], y=player_df[y_axis], mode='lines', line=dict(color='gray', width=2), showlegend=False))
        # extract the legend from the figure
        legend = fig['layout']['legend']
        # remove the legend from the figure
        fig.update_layout(showlegend=False)
        # update the color of the points to be the same as the team color
        change_to_team_colors(fig, player_df, team_colors)
        fig.update_traces(marker=dict(size=15, line=dict(width=3)))
        adjust_axes(fig, player_df, x_axis, y_axis)
        figs.append(fig)
        set_axis_text(fig)
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    with c1:
        st.plotly_chart(figs[0], use_container_width=True)
    with c2:
        st.plotly_chart(figs[1], use_container_width=True)
    with c3:
        st.plotly_chart(figs[2], use_container_width=True)
    with c4:
        st.plotly_chart(figs[3], use_container_width=True)
    # TODO: show the legend on the right side of the plots

# TODO: st.multiselect, st.pills may be a good tool to use for the comparing stats