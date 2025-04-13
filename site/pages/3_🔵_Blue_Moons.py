import streamlit as st
import os, pandas as pd

# SET PAGE CONFIG
st.set_page_config(page_title='Blue Moons!',
                   page_icon='🔵',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('Blue Moons!')

# read through the leaders directory and get the csv files
leaders_dir = '/mnt/d/github/Basketball_Scraping/site/leaders/'

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

for tab, csv in zip(tabs,csv_names):
    with tab:
        # display the dataframe in the tab
        st.dataframe(dfs[csv], use_container_width=True, use_container_height=True, hide_index=True)

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