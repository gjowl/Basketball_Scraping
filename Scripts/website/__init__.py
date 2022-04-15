from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'akdj jdlkfa' #look up what this is actually for, something about cookies

    from .views import views
    from .auth import auth
 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')#the prefix is how you access all of the urls for this route (if you add a route ,)
 
    return app
