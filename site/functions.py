import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os

def change_to_team_colors(_fig, _data, team_colors):
    # set the color for each player to be the same as their team color
    for i in range(len(_data)):
        # get the team abbreviation and match it to the hexcolors file
        team = _data['TEAM_ABBREVIATION'][i]
        # get the color from the team_colors file
        color1 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
        _fig.data[i].marker.color = color1
        color2 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 2'].values[0]
        # change the color of the outline to be the same as the team color
        _fig.data[i].marker.line.color = color2

# sort and show the data
def sort_and_show_data(_data, _col1, _team_colors, _descriptor, _sort_bottom=False, n=10):
    # sort the data by the stat
    top = _data.sort_values(by=_col1, ascending=_sort_bottom).head(n)
    top = top.reset_index(drop=True)
    # add the player name and team abbreviation to the hover template
    hovertemplate = [f'{top["TEAM_ABBREVIATION"][i]} | {top["PLAYER_NAME"][i]}<extra></extra>' for i in range(len(top))]
    fig = px.bar(top, x='PLAYER_NAME', y=_col1, color='PLAYER_NAME', title=f'{_descriptor} {n} Players - {_col1}', labels={'x': 'Player Name', 'y': _col1})
    for i in range(len(top)):
        # add the hover template to the bar
        fig.data[i].hovertemplate = hovertemplate[i]
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    # fit the figure to the screen
    fig.update_layout(yaxis=dict(range=[0, top[_col1].max() * 1.1]), xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    # remove the legend
    fig.update_traces(marker=dict(line=dict(width=4, color='black')))
    fig.update_layout(showlegend=False)
    change_to_team_colors(fig, top, _team_colors)
    # set the surrounding lines to be bigger
    set_axis_text(fig)
    #st.plotly_chart(fig, use_container_width=True)
    return top, fig

# plot the scatter plot of the stat vs the sort column
# TODO: could eventually highlight players who are in their first, second, third etc. years in the league in gold?
def plot_quadrant_scatter(_data, _col1, _col2, _top, _team_colors):
    # calculate the average of the stat
    avg = _data[_col1].mean()
    # get the difference from the average
    avg_sort = _data[_col2].mean()
    # plot the data
    fig = px.scatter(_data, x=_col1, y=_col2, color='PLAYER_NAME', title=f'{_col1} vs {_col2}')
    # add a line at 0 for both axes
    fig.add_hline(y=avg_sort, line_color='dodgerblue', line_width=1, line_dash='dash')
    fig.add_vline(x=avg, line_color='red', line_width=1, line_dash='dash')
    fig.update_traces(marker=dict(size=10))
    # remove the legend
    fig.update_layout(showlegend=False)
    # set all points to gray
    fig.update_traces(marker=dict(color='gray', line=dict(width=1, color='black')))
    # highlight the top players in the scatter plot
    for i in range(len(_top)):
        # get the player name and team abbreviation
        player = _top['PLAYER_NAME'][i]
        team = _top['TEAM_ABBREVIATION'][i]
        # color the player name and team abbreviation
        color1 = _team_colors[_team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
        color2 = _team_colors[_team_colors['TEAM_ABBREVIATION'] == team]['Color 2'].values[0]
        # find the player in the data and set the color to the team color
        player_index = _data[_data['PLAYER_NAME'] == player].index[0]
        fig.data[player_index].marker.color = color1
        fig.data[player_index].marker.line.color = color2
        # change the zorder to be higher than the rest of the points
        fig.data[player_index].marker.line.width = 3
        fig.data[player_index].marker.size = 15
        #fig.data[player_index].hovertemplate = hovertemplate[player_index]
        # TODO: bring the point in front of others instead of just making bigger like above
    # write the average above the yaxis line
    max_x = _data[_col1].max()
    max_y = _data[_col2].max()
    set_axis_text(fig)
    #adjust_axes(fig, _data, _col1, _col2)
    #fig.add_annotation(x=max_x, y=0, text=f'Avg {_col1} = {avg:.2f}', showarrow=False, font=dict(size=16), yshift=10)
    #fig.add_annotation(x=max_x, y=max_y, text=f'Avg {_col2} = {avg_sort:.2f}', showarrow=False, font=dict(size=16), xshift=10)
    st.plotly_chart(fig, use_container_width=False)

# loop through the year_data_dictionary and get all the data for the player
def get_player_data(_year_data_dict, _player):
    output_df = pd.DataFrame()
    for key in _year_data_dict.keys():
        # get the data for the player
        tmp_df = _year_data_dict[key][_year_data_dict[key]['PLAYER_NAME'] == _player]
        # check if the dataframe is empty, if so skip it
        if tmp_df.empty:
            continue
        # add the year to the dataframe
        tmp_df['YEAR'] = key
        output_df = pd.concat([output_df, tmp_df], axis=0)
        # move year to the front of the dataframe
        output_df = output_df[['YEAR'] + [col for col in output_df.columns if col != 'YEAR']]
        # replace the index column with the year column
        output_df = output_df.reset_index(drop=True)
    return output_df

# adjusts the axes values to be within the range of the data
def adjust_axis(_fig, _data, _col):
    min_col, max_col = _data[_col].min(), _data[_col].max()
    min_col, max_col =  min_col-(min_col*0.1), max_col+(max_col*0.1)
    if min_col <= 1:
        min_col = 0
    return min_col, max_col

# adjusts the axes values to be within the range of the data
def adjust_axes(_fig, _data, _xcol, _ycol):
    min_x, max_x = _data[_xcol].min(), _data[_xcol].max()
    min_y, max_y = _data[_ycol].min(), _data[_ycol].max()
    min_x, max_x =  min_x-(min_x*0.1), max_x+(max_x*0.1)
    min_y, max_y =  min_y-(min_y*0.1), max_y+(max_y*0.1)
    # TODO: if you can, remove the y-axis tick at if the min is the same for x and y
    if min_y <= 1:
        min_y = 0
    if min_x <= 1:
        min_x = 0
    _fig.update_yaxes(range=[min_y, max_y])
    _fig.update_xaxes(range=[min_x, max_x])

# get the player ranks for the stats
def get_player_ranks(_data, _player, _stat_list):
    player_ranks = pd.DataFrame()
    for stat in _stat_list:
        # calculate the percentile for each stat
        _data[f'{stat}_Percentile'] = _data[stat].rank(pct=True)
        ## get the percentile for the stat for the player
        #player_stat = _data[_data['PLAYER_NAME'] == _player][stat].values[0]
        # create a ranked list column based on the percentile of the stat
        _data[f'{stat}_Rank'] = _data[stat].rank(ascending=False)
        # add the percentile and rank to the player_ranks dataframe
        player_ranks[stat] = [_data[_data['PLAYER_NAME'] == _player][f'{stat}_Percentile'].values[0], _data[_data['PLAYER_NAME'] == _player][f'{stat}_Rank'].values[0]]
    # transpose the player_ranks dataframe so that the stats are the index and the percentiles and ranks are the columns
    player_ranks = player_ranks.transpose()
    player_ranks.columns = ['Percentile', 'Rank']
    return player_ranks


# set the size of the text in the x and y axes
def set_axis_text(_fig, _x_size=16, _y_size=16):
    additional_size = 2.5
    # update the text size of the x and y axes ticks
    _fig.update_xaxes(tickfont=dict(size=_x_size))
    _fig.update_yaxes(tickfont=dict(size=_y_size))
    # update the text size of the x and y axes titles
    _fig.update_xaxes(title_font=dict(size=_x_size+additional_size))# make this a formula
    _fig.update_yaxes(title_font=dict(size=_y_size+additional_size))
    # change the text to monospaced font
    _fig.update_layout(font_family="monospace")
    _fig.update_layout(title_font=dict(size=_x_size+additional_size*2))

def make_year_scatterplot(_df, _col, _team_colors):
    x_axis = 'SEASON'
    y_axis = _col 
    fig = px.scatter(_df, x=x_axis, y=y_axis, color='YEAR', hover_name='TEAM_ABBREVIATION', title=f'{x_axis} vs {y_axis}')
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='black')))
    fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis)
    # draw a line between consecutive year points
    fig.add_trace(go.Scatter(x=_df[x_axis], y=_df[y_axis], mode='lines', line=dict(color='lightgrey', width=3), showlegend=False))
    # extract the legend from the figure
    legend = fig['layout']['legend']
    # remove the legend from the figure
    fig.update_layout(showlegend=False)
    # update the color of the points to be the same as the team color
    change_to_team_colors(fig, _df, _team_colors)
    fig.update_traces(marker=dict(size=18, line=dict(width=3)))
    min_y, max_y = adjust_axis(fig, _df, y_axis)
    fig.update_yaxes(range=[min_y, max_y])
    # add the average of the stat to the plot (should get these instead for the year data?)
    avg = _df[y_axis].mean()
    fig.add_hline(y=avg, line_color='red', line_width=1, line_dash='dash')
    # add the average to above the x-axis line
    fig.add_annotation(x=_df[x_axis].max(), y=max_y, text=f'Avg {y_axis} = {avg:.2f}', showarrow=False, font=dict(size=16), yshift=10)
    set_axis_text(fig)
    return fig
        
## traverse directory to load data
def create_year_data_dict(_datadir):
    year_data_dict = {}
    for root, dirs, files in os.walk(_datadir):
        for file in files:
            # look if the name of the file is what you want
            # read in the file
            tmp_df = pd.read_csv(os.path.join(root, file))
            # get the filename and remove the extension, separate by _
            filename = file.split('_')[0]
            # check if ~ is in the filename, if so don't add it to the dictionary
            if '~' in filename:
                continue
            # change the YEAR column to be SEASON, keep the split by _
            tmp_df['YEAR'] = filename
            tmp_df['SEASON'] = tmp_df['YEAR'].str.split('-').str[0]
            # add the df to the dictionary with the filename as the key
            year_data_dict[filename] = tmp_df
    return year_data_dict

def annotate_with_emojis(_player_name, _emoji_df):
    # Check if the player name is in the emoji_df
    if _player_name in _emoji_df['PLAYER_NAME'].values:
        # Get the corresponding emoji from the emoji_df
        emoji = _emoji_df.loc[_emoji_df['PLAYER_NAME'] == _player_name, 'Emoji'].values[0]
        link = _emoji_df.loc[_emoji_df['PLAYER_NAME'] == _player_name, 'Link'].values[0]
        return f"{_player_name} [{emoji}]({link})"
    else:
        return _player_name

# check if the emoji players are in the top players list
def emoji_check(_emoji_df, _players_df, col='PLAYER_NAME'):
    players = _players_df[col].tolist()
    emoji_player_list = [player for player in players if player in _emoji_df['PLAYER_NAME'].tolist()]
    _emoji_df = _emoji_df[_emoji_df['PLAYER_NAME'].isin(emoji_player_list)]
    return _emoji_df