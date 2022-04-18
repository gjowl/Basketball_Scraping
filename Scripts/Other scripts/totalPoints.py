# @Author: Gilbert Loiseau
# @Date:   2022/01/07
# @Email:  gjowl04@gmail.com
# @Filename: totalPoints.py
# @Last modified by:   Gilbert Loiseau
# @Last modified time: 2022/04/17


"""
This file is the first project I made to scrape data from pages on
https://www.basketball-reference.com/. I used scrapingExample.py as a template

I'm going to try to scrape and analyze a simple bit of data:
  -get the point totals of all players current and retired, and automatically update
   for current players everyday

This will give me practice in a couple of things that I'll need to do to get this going:
  -scraping data daily
  -updating a file everyday with an increase in points
  -get me started organizing data between current players and retired players
  -start thinking of ways to analyze this point total data over time
    -I'll need to get the years and analyze any trends for progress over time:
     maybe like a graph of longevity showing point totals every year with a graph with all players
     and how long they last in the league (likely just consecutive years, but could also look at
     players who are out of the league for a couple years and see the stats when they get back)
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

#Main
if __name__ == '__main__':
    # URL to scrape
    url = "https://www.basketball-reference.com/"

    # collect HTML data
    html = urlopen(url)

    # create beautiful soup object from HTML
    soup = BeautifulSoup(html, features="lxml")

    # get rows from table
    rows = soup.findAll('tr')[2:]
    rows_data = [[td.getText() for td in rows[i].findAll('td')]
                        for i in range(len(rows))]# if you print row_data here you'll see an empty row
                        # so, remove the empty row
    rows_data.pop(20)# for simplicity subset the data for only 39 seasons
    rows_data = rows_data[0:38]

    #test 2
