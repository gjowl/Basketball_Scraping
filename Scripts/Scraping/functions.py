from urllib.request import urlopen

# https://github.com/microsoft/WSL/issues/5126: helped with problems installing chromium
# which was necessary for using chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import player
import os

def makeOutputDir(outputDir):
    # check if the path to the directory exists
    if not os.path.isdir(outputDir):
        print('Creating output directory: ' + outputDir + '.')
        # the below makes directories for the entire path
        os.makedirs(outputDir)
    else:
        print('Output Directory: ' + outputDir + ' exists.')

def getTableNames(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.binary_location = ("/mnt/c/Program Files/Google/Chrome/Application/chrome.exe")
    # Set path to chromedriver as per your configuration
    webdriver_service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=webdriver_service, chrome_options=options)
    driver.close()
    print('worked')
    exit()
    # collect HTML data
    html = urlopen(url)
    # create beautiful soup object from HTML
    soup = BeautifulSoup(html, features="lxml")
    tables = []
    tables = soup.find_all('table')
    #div = soup.find_all('div', class_='table_wrapped')
    tableIds = []
    for table in tables:
        id = table.get('id')
        print(id)
        tableIds.append(id)
    exit()
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

def scrapeAllPlayers(playersCsv, saveDir):
    # convert csv file to dataframe
    df_players = pd.read_csv(playersCsv, sep=",")
    
    # URL to scrape
    playersUrl = "https://www.basketball-reference.com/players/"

    # getter function
    for name, url in zip(df_players.PlayerName, df_players.Url):
        #TODO: it will lock me out if I have too many requests per second, so I'll have to add in a wait time
        # append player url with url of each player
        urlToSearch = playersUrl+url
        
        # Get table names from the website
        tableIds = getTableNames(urlToSearch)

        # convert the types of tables using beautiful soup
        # get all of the dataframes from the webpage (currently only gets 6 (per ones I can't seem to pull out yet))
        df_dict = getTablesAsDataframes(tableIds, urlToSearch)
        print(name)
        
        dataFile = saveDir+'/' + name + '.csv'
        
        # loop through all dataframes 
        for id, df in df_dict.items():
            #loop through the years in each dictionary
            print(id)
            print(df.head())
            colNames = df.columns
            #df.to_csv(dataFile)
            #for index, row in df.iterrows():
            #    # loop through all columns and add to year data 
            #    for col in colNames:
            #        data = df.at[index,col]
            #        print(data)
        exit()
        #TODO: think of good ways to save this data for all players: name of the spreadsheet is the name of the table?
        # I just decided to read about the terms of use, and looks like I can't actually create a website using this data (and maybe not even results of this data? Not sure though.
        # At the very least, I can blog/create content about this stuff as I find it using data from basketball reference as a source?) And this scraper is a nice piece of software
        # for others as well! At the least I'll have a real life experience coding project under my belt.
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        print(titles)
