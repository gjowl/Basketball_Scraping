#equivalent to calling from website import db if we were outside of this dir
# the . imports from this directory
from . import db

# custom class that will give our user object some characteristics for our user object
from flask_login import UserMixin

# allows sqlalchemy to add the current date and time whenever a new note is made
from sqlalchemy.sql import func

#The below are database models (all of the users, notes, etc. MUST look like the below)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # stores the timezone and date information for 
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # foreign key is a column in a database that references a column in another database
    # Must give a valid user.id for every created note: allows you to create multiple notes
    # for a single user, allowing you to be able to reference each users created note
    # if curious about how this works, look up html 1 to many/1 to 1/1 to user/etc. referenced
    # around the 1:28 mark in the video (foreign key relationships)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
class User(db.Model, UserMixin):
    #define all the columns that are going to be found for this user
    # primary key is a unique way to identify users (unique integer identifier
    # for each user); when initialized database automatically makes a new one
    id = db.Column(db.Integer, primary_key=True)
    # .String() limits the size of string allowed. Unique means it must be completely
    # unique to any other users
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    #Note field that allow you to access all of that users notes
    notes = db.relationship('Note')