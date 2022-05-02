
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import player

def getTableNames(url):
    # collect HTML data
    html = urlopen(url)
    # create beautiful soup object from HTML
    soup = BeautifulSoup(html, features="lxml")

    # get all the tables from the page
    tables = soup.find_all('table')
    #div = soup.find_all('div', class_='table_wrapped')
    tableIds = []
    for table in tables:
        id = table.get('id')
        tableIds.append(id)
    return tableIds

def getTablesAsDataframes(tableNames, url):
    df_dict = {}
    for name in tableNames:
        list_of_df = pd.read_html(url, attrs={'id':name}, flavor='bs4')
        for df in list_of_df:
            df_data = pd.DataFrame(df)
            #make a dictionary with id and dataframe (named list)
            df_dict[name] = df_data #.append to update
    return df_dict

def scrapeAllPlayers():
    #TODO: make a way to get every single player from every single team ever and scrape the total points scored value
    # may be a little difficult: have to go to url for each player? or can I type a search into the bar or something?
    # I got a csv file of data from bballreference: playersFromBasketballReference.csv
    dataDir = "/mnt/c/Users/gjowl/github/Basketball_Scraping/Data files/"
    playersCsv = dataDir+"playersUpdated.csv"
    df = pd.read_csv(playersCsv, sep=",")
    
    # URL to scrape
    playersUrl = "https://www.basketball-reference.com/players/"

    # getter function
    for url in df["Url"]:
        #TODO: it will lock me out if I have too many requests per second, so I'll have to add in a wait time
        # append player url with url of each player
        urlToSearch = playersUrl+url
        
        # Get table names from the website
        tableIds = getTableNames(urlToSearch)
        print(tableIds)

        # convert the types of tables using beautiful soup
        # get all of the dataframes from the webpage (currently only gets 6 (per ones I can't seem to pull out yet))
        df_dict = getTablesAsDataframes(tableIds, urlToSearch)
        print(df_dict) 
        # create the player
        #player = player.player

        # loop through all dataframes 
        for name, df in df_dict.items():
            #loop through the years in each dictionary
            print(name)
            print(df.head())
            print(df.columns)
            colNames = df.columns
            for index, row in df.iterrows():
                #season = df.at[index,'Season']
                #year = year.year(season)
                # loop through all columns and add to year data 
                for col in colNames:
                    data = df.at[index,col]
                    print(data)
                    # add year data to player data
                    #year.add(col, data)
        #TODO: think of good ways to save this data for all players: name of the spreadsheet is the name of the table?
        # I just decided to read about the terms of use, and looks like I can't actually create a website using this data (and maybe not even results of this data? Not sure though.
        # At the very least, I can blog/create content about this stuff as I find it using data from basketball reference as a source?) And this scraper is a nice piece of software
        # for others as well! At the least I'll have a real life experience coding project under my belt.

        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        print(titles)

        #per_game = soup.find("table", {"id":'per_game'})

        #notes on automation for this script:
        """
        for everyday:
            - scrape current list against the new list of players from bball reference and compare; if new, flag
            - scrape data for players who are playing the day before
            - scrape boxscores; if new, flag
            - scrape data for the current 450ish players who are in the league every day
                - for efficiency, maybe make a csv to update for the year? Not for all data
        """