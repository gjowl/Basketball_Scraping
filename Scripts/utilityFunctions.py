import pandas as pd

def convertToUrl(df):
    playerNames = []
    urls = []
    for name in df["Player"]:
        #When I get player names from Basketball Reference, they come as the name attached the the url
        #The below gets the index of the \ so that I can separate this for each added name
        index = name.index('\\')
        playerName = name[:index]
        midUrl = name[index+1:index+2]
        endUrl = name[index+1:]
        url = midUrl+"/"+endUrl+".html"
        playerNames.append(playerName)
        urls.append(url)
    return playerNames, urls

def convertToUrlFormat(dir, origFile, newFile):
    #addURLInfo() make this into a function to add in the url info to the file
    #Read in player name list
    df = pd.read_csv(origFile, sep=",")
    # get the player names and urls from the original file
    playerNames, urls = convertToUrl(df)
    del df["Player"]
    #insert the player names list as first column
    df.insert(0, 'PlayerName', playerNames)
    #insert the url list as second column
    df.insert(1, 'Url', urls)
    #write the new file
    df.to_csv(dir+"playersUpdated.csv")