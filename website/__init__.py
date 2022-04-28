from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
#helps manage all login related items
from flask_login import LoginManager

#the below object is where we will be storing user data
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'akdj jdlkfa' #look up what this is actually for, something about cookies
    
    #SQL Alchemy database is stored at this spot
    # f allows the things inside brackets to be evaluated as a string
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    #initialize the database defined above and this app is what we will be using for it
    db.init_app(app)

    
    from .views import views
    from .auth import auth
 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')#the prefix is how you access all of the urls for this route (if you add a route ,)
 
    from .models import User, Note

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # below is saying to use the function to lead the user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    #change this if the folder is not called website; check if database exists
    if not path.exists('website/' + DB_NAME):
        #creates the database if it doesn't yet exist; creates it in the SQL Alchemy database spot directed by the app on line 15
        db.create_all(app=app)
        print('Created database!')