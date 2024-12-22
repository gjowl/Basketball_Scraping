import streamlit as st
import os, pandas as pd

st.title('last n games')

# VARIABLES

# FUNCTIONS

# MAIN
st.write('This page looks compare stats from the last 5, 10, 15, 20, 25, and 30 games played!')
st.write('You can also select either 1 or all games to see analysis on the previous game or full season statistics up to this point!')

# add in a slider for the number of games to compare
num1, num2 = st.select_slider('Number of games to analyze:',
    options=[1, 5, 10, 15, 20, 25, 30, "all"],
    value=(1,"all"))

# input directory where data is stored
dataDir = '/mnt/h/NBA_API_DATA/BOXSCORES/2024-12-20'

# get the data
for root, dirs, files in os.walk(dataDir):
    for file in files:
        if num1 in file:
            data1 = pd.read_csv(os.path.join(root, file))
        if num2 in file:
            data2 = pd.read_csv(os.path.join(root, file))
        else:
            continue
        
# TODO: get large differences between the two dataframes for each player