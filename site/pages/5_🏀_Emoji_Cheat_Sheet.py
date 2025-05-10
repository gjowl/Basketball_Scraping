import streamlit as st
import os, pandas as pd

cwd = os.getcwd()
cheat_sheet = f'{cwd}/site/emoji_cheat_sheet.csv'

# read in the csv file
cheat_sheet_df = pd.read_csv(cheat_sheet)

# MAIN

st.title('Emoji Cheat Sheet')
st.write('''
         **This is a cheat sheet for emojis used in the website!**\n
         **I thought it would be nice to share facts about players in a fun way, so I added emojis to over 200 players!**\n
         **Some of these emojis can describe the same player, but each player only has one emoji associated with them (ex. Manu Gi).**\n
         **There are also a set of x players that have their own special emoji, usually tied to one of their basketball-reference nicknames (ex: Lebron James ).**\n
         ''')

# Display the cheat sheet
st.dataframe(cheat_sheet_df, use_container_width=True, hide_index=True)