import streamlit as st
import altair as alt
import os, pandas as pd

# SET PAGE CONFIG
st.set_page_config(page_title='Blue Moons!',
                   page_icon='🔵',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Blue Moons!')

# read through the leaders directory and get the csv files
leaders_dir = '/mnt/d/github/Basketball_Scraping/site/leaders/'

# Page Setup








# get the list of csv files in the directory
csv_files = [f for f in os.listdir(leaders_dir) if f.endswith('.csv')]

# make a dictionary to hold the dataframes
dfs = {}
# get the names of all the CSV files in the directory
csv_names = []
for f in csv_files:
    # read in the csv file and add it to the dictionary
    csv_name = f.split('.')[0]
    csv_names.append(csv_name)
    df = pd.read_csv(os.path.join(leaders_dir, f))
    dfs[csv_name] = df

# make those names into a list of tabs
tabs = st.tabs(csv_names)

if st.toggle("Show Simplified DataFrames", key="show_df", value=True):
    for tab, csv in zip(tabs,csv_names):
        with tab:
            cols = ['Player', csv, 'Date']
            # check if the csv is 'REB' and if so, add the 'Result' column
            if csv != 'REB':
                cols.append('Result')
            # if the csv is '3PM', add the '3PA' column next to it
            if csv == '3PM':
                cols.insert(2, '3PA')
                # graph the 3PM vs 3PA as an altair chart with wins and losses as a bar graph below
                points = (alt.Chart(dfs[csv])
                    .mark_circle(size=60, opacity=0.5, color='blue')
                    .encode(x='3PA', y='3PM', tooltip=['Player', '3PM', '3PA', 'Date', 'Result'])
                    .properties(width=600, height=400)
                )
                bars = (alt.Chart(dfs[csv])
                    .mark_bar(opacity=0.5)
                    .encode(x='Result', y='count(Result)')
                    .properties(width=600, height=200)
                )
                chart = alt.vconcat(points, bars, spacing=5).resolve_scale(y='independent')
                chart = chart.configure_axisX(tickCount=10).configure_axisY(tickCount=11)
                # change the scale of the x axis to be 0-20 and the y axis to be 0-20
                
                st.altair_chart(chart, use_container_width=True)
            df = dfs[csv][cols]
            st.dataframe(df, use_container_width=True, hide_index=True)
else:
    for tab, csv in zip(tabs,csv_names):
        with tab:
            df = dfs[csv]
            st.dataframe(df, use_container_width=True, hide_index=True)


# create a dictionary to hold the dataframes
# rare events...what can I add here? 
# Most 3pt attempts in a game 
# Most 3pt makes in a game
# Most assists in a game 
# Most rebounds in a game
# Most steals in a game
# Most blocks in a game
# Most turnovers in a game
# Most minutes in a game

# The unlikely to ever happen ones
# Most fouls in a game
# Most points in a game
# Most games played in a season
# Most games played in a career
# Most games played in a month

# script compares to the current csv file, checks these cats, then updates the main csv if is different (adds in the date, previous change, etc.)
# this is mostly just a look up table; so I think I'm just going to get those tomorrow when all games are going

# Citations:

# altair chart? for wins/losses; 3pm vs 3pa and w/l
#