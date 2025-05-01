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
    🏀 **Scatter Plot** - :violet[**Top N**] players in the league for a given stat vs MPG (Minutes Per Game)\n
    🏀 **Quadrant Plot** - :violet[**Top N**] players highlighted against all other players in the league for a given stat (will add the ability to choose :red[**Y-AXIS**] stat in the future)\n
    """
)
st.divider()

## PAGE 2
st.write(
    """
    🔍 Player Rankings
    ===========\n
    **You can search for a player and view their statistical rankings **OR** search for a rank and output the player**\n
    🏀 **PLAYER SEARCH** - Search for a **PLAYER** to make ranking bar graphs for either a :blue[**CHOSEN SEASON**] OR :violet[**ALL TIME**]\n
    🏀 **RANKING SEARCH** - Search for a **RANK** to output a player; currently only be done for :violet[**ALL TIME**]\n
    **Rankings are made by normalizing each stat as a percentile from lowest stat (0) to highest stat (1)**\n
    """
)
st.divider()

## PAGE 3
st.write(
    """
    🦉 Player Comparison
    ===========\n
    **This page allows you to compare the stats of players over the years they have played in the league**\n
    🏀 Select up to :violet[**10 PLAYERS**] to compare simultaneously on scatterplots\n
    🏀 :red[**Y-AXIS**] - Stat Averages \n
    🏀 :blue[**X-AXIS**] - **# of YEARS IN THE LEAGUE** or **SEASON**\n
    """
)
st.divider()

## PAGE 4
st.write(
    """
    📈 Season Trajectories 
    ===========\n
    **You can filter the data by number of seasons in the league and # of games played to see the top performing players against each other over their years in the league.** \n
    **Eventually, I'd like to update this page to identify trends over time according to these data.**
    """
)
st.divider()

## PAGE 5
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

# TODO Section
st.divider()
st.write(
    """
    MAJOR TODOs:
    =========\n
    🏀 **Hide more emojis**\n
    🏀 **A page where draft classes are searchable for the following data: how many players with x number of years in the NBA?**\n
    🏀 **A way to compare the success of draft classes (Ex. 1984 vs 2003 vs 2021: maybe something like # of players who played more than x years in the NBA?)**\n
    🏀 **Scatterplot of data where you highlight players who are in their first, second, third etc. years in the league?**
    🏀 **Al Horford vs Kevin Love vs Myles Turner vs Thad Young vs Brook Lopez**\n
    🏀 **TJ McConnell vs Jose Alvarado vs Andre Miller**
    """
)
# Add in social at the bottom
# General Additions below
# TODO: could have a story on each page of my love for basketball?
# TODO: add in thoughts that you feel are important to this project here
## TODO: a draft class section? to compare players of the same class
## TODO: add in a section with the oldest players and the number of years they've played for the