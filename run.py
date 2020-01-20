import os
from os import path, walk
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from flask_sqlalchemy import SQLAlchemy 
import sqlite3
from register import registration, register
from logout import logoutuser, logout
from login import loginpage, login
from stats import stat, stats
from lumberjack import log

extra_dirs = ['templates/', ] #reload html templates when saved, while app is running
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

app = Flask(__name__, static_url_path='', static_folder="static", template_folder="templates")
app.secret_key = 'Slskdjf2iu3#1!'
app.config['SQLALCHEMY_ECHO'] = True  ## show sql for debugging
#db = SQLAlchemy() ## may not be needed

app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(stats)
app.register_blueprint(logout)

routes = Blueprint('routes', __name__) # support for addtl py pages

@app.errorhandler(404) # redirect to main page if not found
def page_not_found(e):
    return redirect("/")

@app.route('/', methods=['GET', 'POST']) # main page route
def logina():
    if session.get('logged_in') == True:
        return render_template('main.html')
    else:
        return loginpage()

@app.route('/login', methods=['GET', 'POST']) # redirect to main if logged in
def loggedin():
    if session.get('logged_in') == True: # 
        return redirect('/')
    else:
        return loginpage() # else redirect to login page

@app.route('/register', methods=['GET', 'POST']) # redirect to main page if already logged in
def beginr():
    if session.get('logged_in') == True:
        return redirect('/')
    else:
        return registration()

@app.route('/logout', methods=['GET', 'POST']) # redirect to logout function to strip session variable in cookie
def beginlogout():
    return logoutuser()

@app.route('/stats', methods=['GET', 'POST'])
def beginst():
    if session.get('logged_in'):
        return stat()
    else:
        return redirect("/")

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True #reload html templates when saved, while app is running
    app.run(host='0.0.0.0', debug=True)