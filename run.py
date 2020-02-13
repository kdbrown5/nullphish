import os
from os import path, walk
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from flask_sqlalchemy import SQLAlchemy 
import sqlite3
from register import registration, register
from logout import logoutuser, logout
from login import loginpage, login
from stats import stat, stats, waitforrecdel, waitforrecdel1
from lumberjack import log
from profile import myprofile, profile
from gophishing import gophishing, gophish
from fy import fy, apiid
from topic1 import topic1, topic11

extra_dirs = ['templates/', ] #reload html templates when saved, while app is running
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

app = Flask(__name__, static_url_path='', static_folder="static", template_folder="templates", subdomain_matching=True)

app.config['SERVER_NAME'] = "nullphish.com"
app.config['app'] = "app.nullphish.com"
app.secret_key = 'Slskdjf2iu3#1!'
app.config['SQLALCHEMY_ECHO'] = True  ## show sql for debugging
#db = SQLAlchemy() ## may not be needed

app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(stats)
app.register_blueprint(logout)
app.register_blueprint(profile)
app.register_blueprint(gophishing)
app.register_blueprint(fy)
app.register_blueprint(topic1)

routes = Blueprint('routes', __name__) # support for addtl py pages

@app.errorhandler(404) # redirect to main page if not found
def page_not_found_public(e):
    return redirect("/")

@app.route('/', methods=['GET', 'POST']) # main page route
def logina():
    return render_template('public.html')


@app.route('/', subdomain="app", methods=['GET', 'POST']) # main page route
def loginb():
    if session.get('logged_in') == True:
        return render_template('main.html')
    else:
        return loginpage()

@app.route('/login', subdomain="app", methods=['GET', 'POST']) # redirect to main if logged in
def loggedin():
    if session.get('logged_in') == True: # 
        return redirect('/')
    else:
        return loginpage() # else redirect to login page

@app.route('/register', subdomain="app", methods=['GET', 'POST']) # redirect to main page if already logged in
def beginr():
    return registration()

@app.route('/logout', subdomain="app", methods=['GET', 'POST']) # redirect to logout function to strip session variable in cookie
def beginlogout():
    return logoutuser()

@app.route('/profile', subdomain="app", methods=['GET', 'POST'])
def beginp():
    if session.get('logged_in'):
        return myprofile()
    else:
        return redirect('/')

@app.route('/stats', subdomain="app", methods=['GET', 'POST'])
def beginst():
    if session.get('logged_in'):
        if session.get('role') == 'superadmin' or 'admin':
            return stat()
    else:
        return redirect("/")

@app.route('/stats/del', subdomain="app", methods=['GET', 'POST'])
def beginstatdel():
    return waitforrecdel()

@app.route('/stats/mod', subdomain="app", methods=['GET', 'POST'])
def beginstatdel1():
    return waitforrecdel1()

@app.route('/gophishing', subdomain="app", methods=['GET', 'POST']) # main page route
def loginp():
    if session.get('logged_in') == True:
        return gophish()
    else:
        return loginpage()

@app.route('/fy', subdomain="app", methods=['GET', 'POST']) # redirect to main if logged in
def logid():
    return apiid() # else redirect to login page

@app.route('/education/topic1', subdomain="app", methods=['GET', 'POST'])
def topic1m():
    if session.get('logged_in'):
        return topic11()
    else:
        return redirect("/")

#### template iframe rendering for gophishing template preview
@app.route('/templates/amazon.html', subdomain="app", methods=['GET', 'POST']) 
def amazontemplate():
    return render_template('amazon.html')

@app.route('/templates/prototype2.html', subdomain="app", methods=['GET', 'POST']) 
def prototype2template():
    return render_template('prototype2.html')

@app.route('/templates/starbucks.html', subdomain="app", methods=['GET', 'POST']) 
def starbuckstemplate():
    return render_template('starbucks.html')
######################## end template render

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True #reload html templates when saved, while app is running
    app.run(host='0.0.0.0', debug=True)