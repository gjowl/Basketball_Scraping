import streamlit as st
import os, pandas as pd

# SET PAGE CONFIG
st.set_page_config(page_title='Blue Moons!',
                   page_icon='🔵',
                   layout='wide',
                   initial_sidebar_state='auto')

st.title('In the works!')

# rare events...what can I add here? 
# this may at first just be a list of things that could change, and whenever they do, they get updated here
# Most 3pt attempts in a game
# Most 3pt makes in a game
# Most assists in a game
# Most rebounds in a game
# Most steals in a game
# Most blocks in a game
# Most turnovers in a game
# Most fouls in a game
# Most points in a game
# Most minutes in a game
# Most games played in a season
# Most games played in a career
# Most games played in a month

# script compares to the current csv file, checks these cats, then updates the main csv if is different (adds in the date, previous change, etc.)