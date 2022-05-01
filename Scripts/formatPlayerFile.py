from utilityFunctions import convertToUrlFormat

#TODO: make this automatic and updating
dataDir = "/mnt/c/Users/gjowl/github/Basketball_Scraping/Data files/"
allPlayersCsv = dataDir+"playersFromBasketballReference.csv"
newCsv = dataDir+"playersUpdated.csv"

convertToUrlFormat(dataDir, allPlayersCsv, newCsv)