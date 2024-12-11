

"""
Looking through some of my coding ideas, I found this appealing one: essentially, I want to be able to
calculate a way to determine the "winners" of trades. I want to be able to look at a trade and say
"this team won this trade" or "this team lost this trade" and why. My starting idea is to look at a
trade and determine the win shares added for a team in the trade. A good one to start with is the
Nets and Celtics trade from 2013, where the Nets traded Gerald Wallace, Kris Humphries, and MarShon
Brooks for Kevin Garnett, Paul Pierce, and Jason Terry and picks. 

I think most people would clearly say that the Celtics won this trade, but I want to be able to quantify
it. I will start by looking at win shares, but then potentially add in all star appearances after the trade,
seasons of relevance after the trade, etc.

TODO:
- get the data for the trade
    - win shares, all star appearances, etc.
- calculate the win shares added for each team

eventually, maybe I could do this for lots of trades and determine some factors that seem to be important, run 
regression on them, and then use that to determine the winners of trades, both in the moment, and with future potential.

"""

