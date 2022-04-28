# @Author: Gilbert Loiseau
# @Date:   2022/04/17
# @Filename: totalPointsFunctions.py
# @Last modified by:   Gilbert Loiseau
# @Last modified time: 2022/04/17


"""
This file contains functions for my totalPoints code.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def scrapeTotalPoints():
    #TODO: make a way to get every single player from every single team ever and scrape the total points scored value
    # may be a little difficult: have to go to url for each player? or can I type a search into the bar or something?
    # I got a csv file of data from bballreference: playersFromBasketballReference.csv
    # TODO: I should work on a way to update this automatically each year
    allPlayersCSV = "/mnt/c/Users/gjowl/github/Basketball_Scraping/Data files/playersFromBasketballReference.csv"

    #addURLInfo() make this into a function to add in the url info to the file
    #Read in player name
    allPlayers = pd.read_csv(allPlayersCSV, sep=",")
    print(allPlayers)


    for name in allPlayers["Player"]:
        #When I get player names from Basketball Reference, they come as the name attached the the url
        #The below gets the index of the \ so that I can separate this for each added name
        index = name.index('\\')
        print(name[index:])
        
    #Pass through getter Function 
   
    # URL to scrape, notice f string:
    playersUrl = f"https://www.basketball-reference.com/players/"
    print(playersUrl)
    #add first letter of name
    #add the name string for the player
    #url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

    ## collect HTML data
    #html = urlopen(url)
    
    # Output points (but set this up so that I can eventually just output whatever info I want from their webpage)
    # TODO: get a list of all of the different stats found on basketball reference
"""
    final_df = pd.DataFrame(columns = ["Year", "Team", "W", "L",
                                       "W/L%", "GB", "PS/G", "PA/G",
                                       "SRS", "Playoffs",
                                       "Losing_season"])
    # loop through each year
    for y in years:        # NBA season to scrape
        year = y

        # URL to scrape, notice f string:
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

        # collect HTML data
        html = urlopen(url)

        # create beautiful soup object from HTML
        soup = BeautifulSoup(html, features="lxml")

        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

        # first, find only column headers
        headers = titles[1:titles.index("SRS")+1]

        # then, exclude first set of column headers (duplicated)
        titles = titles[titles.index("SRS")+1:]

        # next, row titles (ex: Boston Celtics, Toronto Raptors)
        try:
            row_titles = titles[0:titles.index("Eastern Conference")]
        except: row_titles = titles
        # remove the non-teams from this list
        for i in headers:
            row_titles.remove(i)
        row_titles.remove("Western Conference")
        divisions = ["Atlantic Division", "Central Division",
                     "Southeast Division", "Northwest Division",
                     "Pacific Division", "Southwest Division",
                     "Midwest Division"]
        for d in divisions:
            try:
                row_titles.remove(d)
            except:
                print("no division:", d)

        # next, grab all data from rows (avoid first row)
        rows = soup.findAll('tr')[1:]
        team_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]
        # remove empty elements
        team_stats = [e for e in team_stats if e != []]
        # only keep needed rows
        team_stats = team_stats[0:len(row_titles)]

        # add team name to each row in team_stats
        for i in range(0, len(team_stats)):
            team_stats[i].insert(0, row_titles[i])
            team_stats[i].insert(0, year)

        # add team, year columns to headers
        headers.insert(0, "Team")
        headers.insert(0, "Year")

        # create a dataframe with all aquired info
        year_standings = pd.DataFrame(team_stats, columns = headers)

        # add a column to dataframe to indicate playoff appearance
        year_standings["Playoffs"] = ["Y" if "*" in ele else "N" for ele in year_standings["Team"]]
        # remove * from team names
        year_standings["Team"] = [ele.replace('*', '') for ele in year_standings["Team"]]
        # add losing season indicator (win % < .5)
        year_standings["Losing_season"] = ["Y" if float(ele) < .5 else "N" for ele in year_standings["W/L%"]]

        # append new dataframe to final_df
        final_df = final_df.append(year_standings)

    # print final_df
    print(final_df.info)
    # export to csv
    final_df.to_csv("nba_team_data.csv", index=False)
"""