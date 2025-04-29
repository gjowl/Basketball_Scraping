import streamlit as st
import altair as alt
import os, pandas as pd

# SET PAGE CONFIG
st.set_page_config(page_title='Blue Moons!',
                   page_icon='🔵',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('🔵 Blue Moons')

# read through the leaders directory and get the csv files
leaders_dir = '/mnt/d/github/Basketball_Scraping/site/leaders/'

# Page Setup

st.write('''
         **Stats that occur "once in a :blue[blue moon]" are rare events that go down in the history books.**\n
            **This page is dedicated to those rare events (data from Wikipedia).**\n
         ''')
# TODO: need to work on the analysis here
# TODO: add in a way to update these if there's ever a new blue moon (and link it to the home page!)
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
if st.toggle("**Show Simplified DataFrames**", key="show_df", value=True):
    for tab, csv in zip(tabs,csv_names):
        with tab:
            cols = ['Player', csv, 'Date']
            df = dfs[csv][cols]
            st.dataframe(df, use_container_width=True, hide_index=True)
else:
    for tab, csv in zip(tabs,csv_names):
        with tab:
            df = dfs[csv]
            st.dataframe(df, use_container_width=True, hide_index=True)