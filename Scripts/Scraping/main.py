from functions import *

#TODO: make a way to get every single player from every single team ever and scrape the total points scored value
# may be a little difficult: have to go to url for each player? or can I type a search into the bar or something?
# I got a csv file of data from bballreference: playersFromBasketballReference.csv
dataDir = "/mnt/c/Users/gjowl/github/Basketball_Scraping/Data files/"
playersCsv = dataDir+"playersUpdated.csv"

scrapeDataDir = "/mnt/h/Basketball_Reference/"
makeOutputDir(scrapeDataDir)

#Main
if __name__ == '__main__':
    scrapeAllPlayers(playersCsv, scrapeDataDir) 