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
import player

def scrapeTotalPoints():
    #TODO: make a way to get every single player from every single team ever and scrape the total points scored value
    # may be a little difficult: have to go to url for each player? or can I type a search into the bar or something?
    # I got a csv file of data from bballreference: playersFromBasketballReference.csv
    dataDir = "/mnt/c/Users/gjowl/github/Basketball_Scraping/Data files/"
    playersCsv = dataDir+"playersUpdated.csv"
    df = pd.read_csv(playersCsv, sep=",")
    
    # URL to scrape, notice f string:
    playersUrl = "https://www.basketball-reference.com/players/"
    print(playersUrl)

    #Pass through getter Function 
    for url in df["Url"]:
        urlToSearch = playersUrl+url

        print(url) 
        print(urlToSearch) 
        # collect HTML data
        html = urlopen(urlToSearch)
        #html = urlopen(eval("f'{}'".format(urlToSearch)))

        tableIds = []        
        # convert the types of tables from beautiful soup
        # create beautiful soup object from HTML
        soup = BeautifulSoup(html, features="lxml")

        # get all the tables from the page
        tables = soup.find_all('table')
        #div = soup.find_all('div', class_='table_wrapped')
        #for d in div:
        #    id = div['id']
        #    tableIds.append(id)
        for table in tables:
            id = table.get('id')
            tableIds.append(id)
# search through the url using this to convert dataframes to data

        # get all of the dataframes from the webpage (currently only gets 6 (per ones I can't seem to pull out yet))
        df_dict = {}
        for id in tableIds:
            df = pd.read_html(urlToSearch, attrs={'id':id}, flavor='bs4')
            #make a dictionary with id and dataframe (named list)
            df_dict[id] = df #.append to update
        

        

        # create the player
        #player = player.player

        #for df in df_list:
        for name, data in df_dict.items():
            print(name)
            print(data)
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        print(titles)

        #per_game = soup.find("table", {"id":'per_game'})
        ## prin
        #for t in table:
        #    df = pd.DataFrame(columns=titles)
        #    for row in t.tbody.find_all('tr'):
        #        columns = row.find_all('td')


        
        
        # first, find only column headers
        headers = titles[1:titles.index("SRS")+1]



        # then, exclude first set of column headers (duplicated)
        #titles = titles[titles.index("SRS")+1:]

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