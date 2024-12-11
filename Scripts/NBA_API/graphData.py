import os, sys, pandas as pd, numpy as np, configparser
import time
import matplotlib.pyplot as plt
from classes.boxScore import boxScore

'''
This code setups the boxscore object and calculates some advanced stats that you might be interested in.

Run as: python3 graphData.py dailyConfig.config
'''

# read in the config file
configFile = sys.argv[1]
config = configparser.ConfigParser()
config.read(configFile)
programName = 'graphData'
dataDir = config[programName]['dataDir']
outputDir = config[programName]['graphDir']

# Functions
def wait(number):
    time.sleep(number)

# plot scatterplots of the above stats
def plotScatter(_df, _xaxis, _yaxis, _dir=outputDir): # default output directory is the one passed in from the command line
    x = _df[_xaxis]
    y = _df[_yaxis]

    # using matplotlib
    plt.scatter(x, y, alpha=0.6, c='white', edgecolors='black', linewidths=0.9)
    # change the font size of the x and y labels
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    # add the x and y labels, away from the axes
    plt.xlabel(_xaxis, fontsize=12, labelpad=15)
    plt.ylabel(_yaxis, fontsize=12, labelpad=15, rotation=0)
    # add a title
    plt.title(f'{_xaxis} vs {_yaxis}')
    # calculate the standard deviation of the x and y values
    x_std = x.std()
    y_std = y.std()
    # draw an x=y line
    plt.plot([0, 1], [0, 1], transform=plt.gca().transAxes, c='black', linestyle='--')

    # save the version without error bars
    plt.tight_layout()
    plt.savefig(f'{_dir}/{_xaxis}_vs_{_yaxis}.png')

    # comment out the below if you don't want the svg
    #plt.savefig(f'{_dir}/{_xaxis}_vs_{_yaxis}.svg')

    # comment out the below if you don't want error bars 
    ## add a trendline
    #z = np.polyfit(x, y, 1)
    #p = np.poly1d(z)
    #plt.plot(x, p(x), 'r--')
    ## add the R^2 value
    #r2 = np.corrcoef(x, y)[0, 1] ** 2
    #plt.text(0.5, 0.5, f'R^2 = {r2}', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    ## grey out the error bars
    #plt.errorbar(x, y, xerr=x_std, yerr=y_std, fmt='none', ecolor='grey', capsize=1, capthick=0.3, alpha=0.5)
    ## save the version with error bars
    #plt.savefig(f'{_dir}/{_xaxis}_vs_{_yaxis}_err.png')

    plt.clf()

# loop through the files in the data directory
for datafile in os.listdir(dataDir):
    # get the file name without the extension
    filename = datafile.split('.')[0]

    # get the file path
    datafile = os.path.join(dataDir, datafile)

    # read in the data as a pandas dataframe
    df = pd.read_csv(datafile)
    
    # initialize the boxscore object
    box = boxScore()

    # set the boxscore
    box.setBoxScore(datafile)

    # define the x and y axes for the scatterplots
    y_axis = ['3PA_G', '2PA_G', 'APG', 'SPG', 'BPG', 'PPG', 'APG', 'SPG', 'BPG']
    x_axis = ['3P%', '2P%', 'AST_TO', 'FT%', 'FT%', 'MPG', 'MPG', 'MPG', 'MPG']

    # define the graph output directory
    graphDir = os.path.join(outputDir, filename)
    # make the output directory if it doesn't exist
    if not os.path.exists(graphDir):
        os.makedirs(graphDir)

    for x, y in zip(x_axis, y_axis):
        # remove any rows with NaN values
        df_xy = df.dropna(subset=[x, y])
        plotScatter(df_xy, x, y, graphDir)

    # name some stats that might be interesting to see preliminary graphs of:
    #  3PA vs 3P% (and/or 3PM)
    #  2PA vs 2P% (and/or 2PM)
    #  AST vs AST/TO
    #  STL vs FT%
    #  BLK vs FT%
    #  PPG vs MIN/G
    #  APG vs MIN/G
    #  SPG vs MIN/G
    #  BPG vs MIN/G
    # eventually add o-rating, d-rating, usage rate, and other advanced stats (LEBRON, DURANT, etc.) etc.