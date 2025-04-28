import streamlit as st

# Page Title
st.title("About")

# Page Description
st.write(
    """
    I put this website together to help me learn about web development and
    data scraping, allowing me to practice dynamic data visualization.\n
    For years I've been interested in the NBA and taking boxscore data and
    finding a way to visualize it for myself\n
    Data is sourced from [NBA.com](https://www.nba.com/stats/leaders) going back to the 1996-97 season.\n
    If you have any questions, comments, or suggestions, please feel free to reach out: gjowl04@gmail.com!\n
    """
)
st.divider()

## PAGE 1
st.write(
    """
    🔝 Season Stats
    ===========\n
    This page allows you to view the **top** players in the league for a **chosen season**.
    """
)
st.divider()

## PAGE 2
st.write(
    """
    🔍 Player Rankings
    ===========\n
    You can search for a player and view their statistical rankings **OR** search for a rank and output the player.\n
    Both searches can be made for a **chosen season** or **all time**.\n
    """
)
st.divider()

## PAGE 3
st.write(
    """
    🦉 Player Comparison
    ===========\n
    This page allows you to compare the stats of players over the years they have played in the league.
    """
)
st.divider()

## PAGE 4
st.write(
    """
    📈 Yearly Graphs 
    ===========\n
    You can filter the data by number of years in the league and games played to see how players have performed over their years in the league. \n
    Eventually, I'd like to update this page to identify trends over time according to these data.
    """
)
st.divider()

## PAGE 5
st.write(
    """
    🔵 Blue Moons 
    ===========\n
    A page dedicated to players who have had rare regular season performances that have stood the test of time in NBA records.\n
    I always wanted to be able to look at the top stats all time, and was able to create this page using data from the Wikipedia pages below.\n 
    [3PM](https://en.wikipedia.org/wiki/List_of_NBA_single-game_3-point_scoring_leaders) 
    [Points](https://en.wikipedia.org/wiki/List_of_NBA_single-game_scoring_leaders) 
    [Assists](https://en.wikipedia.org/wiki/List_of_NBA_single-game_assists_leaders) 
    [Rebounds](https://en.wikipedia.org/wiki/List_of_NBA_single-game_rebounding_leaders) 
    [Blocks](https://en.wikipedia.org/wiki/List_of_NBA_single-game_blocks_leaders) 
    """
)

# Add in social at the bottom
# General Additions below
# TODO: could have a story on each page of my love for basketball?
# TODO: add in thoughts that you feel are important to this project here
## TODO: a draft class section? to compare players of the same class
## TODO: add in a section with the oldest players and the number of years they've played for the