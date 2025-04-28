import streamlit as st

st.set_page_config(page_title='Home',
                   page_icon='🏠',
                   layout='wide',
                   initial_sidebar_state='auto')
st.sidebar.success('Select a page to get started!')

# 
st.write('''
        ⛹🏻⛹🏿‍♂️
        ⛹🏽‍♂️⛹🏾‍♀️⛹🏿⛹🏽‍♀️
        ⛹🏼‍♀️⛹🏽⛹🏻‍♂️⛹🏾‍♀️
🪣🏀
         ''')
st.header('Welcome to my NBA Stats Website!')

# TODO: think of what to add to a home page
# add some details and such in here
st.write('This website is a collection of NBA stats and data visualization built using [Streamlit](https://streamlit.io/).')
st.write('''
         For the **2025-26** season, I hope to add in daily game analysis on this page including but not limited to:\n
            - **Most Points, Assists, Rebounds, Steals, and Blocks** \n
            - **Highest +/-, TS%, and USG%** \n
            - **Statistical Anomalies** (Like Jokic's **30-20-20**, or Luka's *73* point game)\n 
        ''')
st.divider()
st.write('''
        For now, feel free to explore the links on the sidebar to view the data and stats collected from [NBA.com](https://www.nba.com/stats/leaders) (data from **1996-1997** season to **present**).\n
        ''')
# add in credits here (nba, basketball-reference, etc.)

# add in a link to the github repo

# add in a link to my linkedin (gross) and substack
