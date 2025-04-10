import pandas as pd
import streamlit as st
import plotly.express as px

def change_to_team_colors(_fig, _data, team_colors):
    # set the color for each player to be the same as their team color
    for i in range(len(_data)):
        # get the team abbreviation and match it to the hexcolors file
        team = _data['TEAM_ABBREVIATION'][i]
        # get the color from the team_colors file
        color1 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
        _fig.data[i].marker.color = color1
        color2 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 2'].values[0]
        # change the color of the circle outline to be the same as the team color
        _fig.data[i].marker.line.color = color2

# sort and show the data
def sort_and_show_data(_data, _col1, _col2, team_colors, n=10):
    # sort the data by the stat
    top = _data.sort_values(by=_col1, ascending=False).head(n)
    top = top.reset_index(drop=True)
    # trim to only have player name and the stat
    percentile_col = f'Percentile'
    # show the data in a bar graph with player names and the stat above the bar
    fig = px.bar(top, x='PLAYER_NAME', y=_col1, color='PLAYER_NAME', title=f'Top {n} Players - {_col1}', labels={'x': 'Player Name', 'y': _col1})
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    # fit the figure to the screen
    fig.update_layout(yaxis=dict(range=[0, top[_col1].max() * 1.1]), xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    # remove the legend
    fig.update_layout(showlegend=False)
    # make spec for vega-lite charts
    fig1 = px.scatter(top, x=_col2, y=_col1, color='PLAYER_NAME', title=f'{_col2} vs {_col1}', labels={'x': _col2, 'y': _col1}, size=f'{percentile_col}')
    change_to_team_colors(fig1, top, team_colors)
    change_to_team_colors(fig, top, team_colors)
    #fig2 = px.scatter(top, x=_col1, y=newCol, color='PLAYER_NAME', title=f'{_col1} vs {newCol}', labels={'x': _col1, 'y': newCol}, size=f'{percentile_col}')
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.plotly_chart(fig1, use_container_width=False)
    st.button(f'Hide')
    return top

# plot the scatter plot of the stat vs the sort column
def plot_quadrant_scatter(_data, _col1, _col2, _top, team_colors):
    # calculate the average of the stat
    avg = _data[_col1].mean()
    # get the difference from the average
    avg_sort = _data[_col2].mean()
    # plot the data
    fig2 = px.scatter(_data, x=_col1, y=_col2, color='PLAYER_NAME', title=f'{_col1} vs {_col2}')
    # add a line at 0 for both axes
    fig2.add_hline(y=avg_sort, line_color='red', line_width=1, line_dash='dash')
    fig2.add_vline(x=avg, line_color='red', line_width=1, line_dash='dash')
    fig2.update_traces(marker=dict(size=10))
    # remove the legend
    fig2.update_layout(showlegend=False)
    # set all points to gray
    fig2.update_traces(marker=dict(color='gray', line=dict(width=1, color='black')))
    # highlight the top players in the scatter plot
    for i in range(len(_top)):
        # get the player name and team abbreviation
        player = _top['PLAYER_NAME'][i]
        team = _top['TEAM_ABBREVIATION'][i]
        # color the player name and team abbreviation
        color1 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
        # find the player in the data and set the color to the team color
        player_index = _data[_data['PLAYER_NAME'] == player].index[0]
        fig2.data[player_index].marker.color = color1
        # change the color of the circle outline to be the same as the team color
        color2 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 2'].values[0]
        fig2.data[player_index].marker.line.color = color2
    st.plotly_chart(fig2, use_container_width=False)

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

def update_yaxis(_fig, _data, _col):
    min = _data[_col].min()
    max = _data[_col].max()
    min = round(min, 1) - 0.05
    max = round(max, 1) + 0.05
    _fig.update_yaxes(range=[min, max])
