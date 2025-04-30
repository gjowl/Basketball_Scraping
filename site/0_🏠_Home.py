import streamlit as st

st.set_page_config(page_title='Home',
                   page_icon='🏠',
                   layout='wide',
                   initial_sidebar_state='auto')
st.sidebar.success('Select a page to get started!')

# 
st.write('''
🪣 ⛹🏽‍♂️⛹🏾‍♀️⛹🏿⛹🏽‍♀️⛹🏻
🏀
⛹🏾⛹🏼‍♂️⛹🏿‍♂️⛹🏻‍♀️⛹🏼
🏀
⛹🏽⛹🏾⛹🏻‍♂️⛹🏼‍♀️⛹🏽‍♂️
🏀
⛹🏾⛹🏼‍♀️⛹🏽⛹🏻‍♂️⛹🏾
🪣
         ''')
st.header('Welcome to the beginnings of an NBA Stats Website!')

# add some details and such in here
st.write('This website is a collection of NBA Stats and Data Visualization built using **[Streamlit](https://streamlit.io/)**.')
st.write('''
         For the **2025-26** season, I hope to add in daily game analysis on this page including but not limited to:\n
            🏀 **Most Points, Assists, Rebounds, Steals, and Blocks** \n
            🏀 **Highest & Lowest +/-, TS%, USG%, and other Advanced Stats** \n 
            🏀 **Player Stat Trajectories over the Last 5, 10, 15, 20, 25, and 30 Games Played** \n
            🏀 :rainbow[**Statistical Anomalies**] (**>=** 50 point games, 5x5s or close, insane triple doubles (**like 🃏 Jokic's 30-20-20**), random career highs, etc.)\n 
        ''')
st.divider()
st.write('''
        For now, feel free to explore the links on the sidebar to view the visuals and data!\n
        Data collected from **[NBA.com](https://www.nba.com/stats/leaders)** (data from **1996-1997** season to **present**).\n
        ''')
# add in credits here (nba, basketball-reference, etc.)

# add in a link to the github repo

st.divider()
# add in a link to my linkedin (gross) and substack
# TODO: add in buttons or something to link to my links
st.write('''
        EMOJIS to Find:
        👾👑🐜
        🪄🌈🦄🕷️
        🐍🖐🏿🐐🐎
        
⭐😷🪰
🐛🦋
🐌🐢🦥
         ''')
