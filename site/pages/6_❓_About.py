import streamlit as st

# Page Title
st.title("About")

# Page Description
st.write(
    """
    **For years I've been interested in the NBA and taking boxscore data and**
    **finding a way to visualize it for myself!**\n
    **I put this website together to help me learn about web development and data scraping, allowing me to practice dynamic data visualization.**\n
    **Data is sourced from [NBA.com](https://www.nba.com/stats/leaders) going back to the 1996-97 season.**\n
    **Website is built using [Streamlit](https://streamlit.io/).**\n
    **Code is available on [GitHub](https://github.com/gjowl/Basketball_Scraping/tree/test/site).**\n
    **If you have any questions, comments, suggestions, or if you feel like you've found all of the hidden emojis :P, please feel free to reach out: gjowl04@gmail.com!**\n
    """
)
st.divider()

## PAGE 1
st.write(
    """
    🔝 Season Stats
    ===========\n
    **This page allows you to view graphs for :violet[**Top N**] players in the league for a :blue[**CHOSEN SEASON**]**\n
    **Graphs Include:**\n
    🏀 **Bar Graph** - :violet[**Top N**] players in the league for a given stat\n
    🏀 **Quadrant Plot** - :violet[**Top N**] players highlighted against all other players in the league for a given stat (will add the ability to choose :red[**Y-AXIS**] stat in the future)\n
    """
)
st.divider()

## PAGE 2
st.write(
    """
    🦉 Player Comparison
    ===========\n
    **This page allows you to compare the stats of players over the years they have played in the league**\n
    How many seasons did Dirk Nowitzki shoot 3s better than Lebron James?
     - Compare By #YEARS IN LEAGUE: off; select Dirk Nowitzki and Lebron James, select 3P%\n
    
    🏀 Select up to :violet[**10 PLAYERS**] to compare simultaneously on scatterplots\n
    🏀 :red[**Y-AXIS**] - Stat Averages \n
    🏀 :blue[**X-AXIS**] - **# of YEARS IN THE LEAGUE** or **SEASON**\n
    """
)
st.divider()

## PAGE 3
st.write(
    """
    🔍 Player Rankings
    ===========\n
    Go Deeper Questions
    🏀 How many players in the 2024-25 season have played in the league for 10+ years?\n
     - Rank Finder: Turn off Show All Time Ranks, select 2024-25 season, # of games played 0, minimum years in league 10\n
    🏀 Who were the top 5 players in STOCK_PG (steal & blocks per game) in the 2020-21 season who would qualify for player awards (>65 games played)?\n
     - Rank Finder: Turn off Show All Time Ranks, select 2020-21 season, # of games played 65, minimum years in league 0\n
    **You can search for a player and view their statistical rankings **OR** search for a rank and output the player**\n
    🏀 **PLAYER SEARCH** - Search for a **PLAYER** to make ranking bar graphs for either a :blue[**CHOSEN SEASON**] OR :violet[**ALL TIME**]\n
    🏀 **RANKING SEARCH** - Search for a **RANK** to output a player; currently only be done for :violet[**ALL TIME**]\n
    **Rankings are made by normalizing each stat as a percentile from lowest stat (0) to highest stat (1)**\n
    """
)
st.divider()

## PAGE 4
st.write(
    """
    🔵 Blue Moons 
    ===========\n
    **A page dedicated to players who have had rare regular season performances that have stood the test of time in NBA records.**\n
    **I always wanted to be able to look at the top stats all time, and was able to create this page using data from the Wikipedia pages below.**\n 
    **[3PM](https://en.wikipedia.org/wiki/List_of_NBA_single-game_3-point_scoring_leaders)**
    **[Points](https://en.wikipedia.org/wiki/List_of_NBA_single-game_scoring_leaders)**
    **[Assists](https://en.wikipedia.org/wiki/List_of_NBA_single-game_assists_leaders)**
    **[Rebounds](https://en.wikipedia.org/wiki/List_of_NBA_single-game_rebounding_leaders)** 
    **[Blocks](https://en.wikipedia.org/wiki/List_of_NBA_single-game_blocks_leaders)** 
    """
)
st.divider()

# TODO Section
st.write(
    """
    📈 Season Trajectories 
    ===========\n
    """
)
st.divider()

## PAGE 5

st.write(
    """
    MAJOR TODOs:
    =========\n
    🏀 **Hide more emojis**\n
    🏀 **A page where draft classes are searchable for the following data: how many players with x number of years in the NBA?**\n
    🏀 **A way to compare the success of draft classes (Ex. 1984 vs 2003 vs 2021: maybe something like # of players who played more than x years in the NBA?)**\n
    🏀 **Scatterplot of data where you highlight players who are in their first, second, third etc. years in the league?**
    
    🏀**Playoff stat for all pages?**\n
    """
)
# Add in social at the bottom
# General Additions below
# TODO: could have a story on each page of my love for basketball?
# TODO: add in thoughts that you feel are important to this project here
## TODO: a draft class section? to compare players of the same class
## TODO: add in a section with the oldest players and the number of years they've played for the
# an interesting alternate idea (or maybe concurrent) is to basically make the website a scrolling timeline of the player: Kind of like the spotify wrapped, but a timeline of the player with 
# their most important stats and their overall impact on the game? Would some sort of impact on the game metric be interesting? How would I define that just using stats?
# I think I have to start with the most impactful players: Steph is an outlier in 3pt shooting all time. But whenever it started (so he has a large difference in 3PAs to how quickly it gets closer)
# could look at something like that? As if the player is a trendsetter if they are an outlier in a stat and the rest of the league (or at least a certain number of players follows suit?)
