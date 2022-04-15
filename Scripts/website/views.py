"""
This is all of the navigatable items for the website
"""

from flask import Blueprint

#Define that this file has bunch of routes/urls to navigate to 
views = Blueprint('views', __name__)

#This function runs whenever you go to the home (/) page
@views.route('/')
def home():
    return "<h1>test<h1>"