"""
This is all of the navigatable items for the website
"""

from flask import Blueprint, render_template, request, flash, jsonify
#current_user: how account information is stored; can retrieve name, notes, email, etc.
# also a way to use information for a default user
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db
import json
#Define that this file has bunch of routes/urls to navigate to 
views = Blueprint('views', __name__)

#This function runs whenever you go to the home (/) page
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method =='POST':
        # get notes
        note = request.form.get('note')
        # make sure note is at least length 1
        if len(note) < 1:
            flash('Note is too short!', category=error)
        else:
            # creates a note for the current user; set it up so if not signed in, doesn't save the searches or anything for people to access, just for me
            new_note = Note(data=note, user_id=current_user.id)
            # makes new note and commits to the page
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("home.html", user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
def note():
    if request.method =='POST':
        # get notes
        note = request.form.get('note')
        # make sure note is at least length 1
        if len(note) < 1:
            flash('Note is too short!', category=error)
        else:
            # creates a note for the current user; set it up so if not signed in, doesn't save the searches or anything for people to access, just for me
            new_note = Note(data=note, user_id=current_user.id)
            # makes new note and commits to the page
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    #turns the data requested from index.js into a python dictionary object from string
    note = json.loads(request.data)
    # access noteId from the note data
    noteId = note['noteId']
    # find the note from the noteId
    note = Note.query.get(noteId)
    # check if note exists
    if note:
        # check if current user owns the note (security check)
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

