
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from .models import User
from . import db
#allows you to covert a password to something much more secure using a hashing function
#   Example: x -> y
#   but y-> ?
# this prevents you from storing the password in plain text, and only allows you to check if the
# password is right: it never will give you the original password from the hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

#Define that this file has bunch of routes/urls to navigate to 
auth = Blueprint('auth', __name__)

# The below are the urls that can be used for this website
# The methods are the type of http requests that are allowed to be sent to this website
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # query through the users by email to check if there are any users with the same email
        user = User.query.filter_by(email=email).first()
        if user:
            # checks to see if the password matches the stored users password hash
            if check_password_hash(user.password, password):
                flash('Login successful', category='success')
                #remembers the user until logout or website is reset so they don't have to login again
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    data = request.form
    print(data)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
#decorator that allows us to only access this page if logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #Category displays messages in a different color
        user = User.query.filter_by(email=email).first()
        if user:
            # Checks to see if the user already exists
            flash('Email already exists.', category = 'error')
        elif len(email) < 4:
            #Checks to see if the length of the email is allowed
            flash('Email must be greater than 4 characters', category = 'error')
        elif len(username) < 2:
            #Checks to see if the length of the username is allowed
            flash('Username must be greater than 2 characters', category = 'error')
        elif password1 != password2:
            #Checks to see if the given passwords match
            flash('Passwords don\'t match.', category = 'error')
        elif len(password1) < 7:
            #Checks to see if the length of the password is allowed
            flash('Password must be greater than 7.', category = 'error')
        else:
            #create a new user, giving it the input email, username, and hash password generated through the hashing method below
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account create!', category='success')
            #after the account is created, redirect to the following url; if you ever change url in views.home, it will always go there 
            # (only hardcode this if you need to)
            return redirect(url_for('views.home'))
            #add user to database

    return render_template("sign_up.html", user=current_user)