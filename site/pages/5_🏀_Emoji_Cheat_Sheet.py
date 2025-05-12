import streamlit as st
import os, pandas as pd

cwd = os.getcwd()
cheat_sheet = f'{cwd}/site/emoji_cheat_sheet.csv'

# read in the csv file
cheat_sheet_df = pd.read_csv(cheat_sheet)

# MAIN

st.title('Emoji Cheat Sheet')

# Display the cheat sheet
st.dataframe(cheat_sheet_df, use_container_width=True, hide_index=True)

st.write('''
         **This is a cheat sheet for emojis used in the website!**\n
         **I thought it would be a nice fun way to share facts about over 200 players!**\n
         **Each player only has one emoji associated with them (ex. Manu Ginóbili is an Olypmpic Gold medalist [🏅], 
         multitime NBA Champion [💍], Argentinian [🇦🇷], and a 2x All Star [⭐], but is only represented by the [🏅]).**\n
         **Each emoji also acts as a clickable link: sometimes to their basketball-reference page or a unique video (usually highlights or a memorable moment)!**\n
         **Good luck searching :D
         ''')
