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
from educationemail import educationemail, educationemaillobby, email1, email2
from emulateuser import emulateuser, emulatelogin
from adminprofile import adminprofile, loadadminprofile
from educationintro import educationintro, educationintro1

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
app.register_blueprint(adminprofile)
app.register_blueprint(gophishing)
app.register_blueprint(fy)
app.register_blueprint(educationemail)
app.register_blueprint(emulateuser)
app.register_blueprint(educationintro)

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
        if session.get('role') == 'admin':
            return render_template('adminlobby.html')
        elif session.get('role') == 'superadmin':
            return render_template('adminlobby.html')
        else:
            return render_template('main.html')
    else:
        return loginpage()

@app.route('/adminprofile', subdomain="app", methods=['GET', 'POST']) # redirect to main if logged in
def rediradminprofile():
    if session.get('logged_in') == True:
        if session.get('role') == 'superadmin':
            return loadadminprofile()
        elif session.get('role') == 'admin':
            return loadadminprofile()
        else:
            return redirect('/profile')
    else:
        return redirect('/login') # else redirect to login page


@app.route('/emulateuser', subdomain="app", methods=['GET', 'POST']) # redirect to main if logged in
def loginemulate():
    if session.get('logged_in') == True:
        if session.get('role') == 'superadmin':
            return emulatelogin()
    else:
        return loginpage() # else redirect to login page

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
    if session.get('logged_in') == True:
        if session.get('role') == 'superadmin':
            return redirect('/adminprofile')
        elif session.get('role') == 'admin':
            return redirect('/adminprofile')
        else:
            return myprofile()
    else:
        return redirect('/login') # else redirect to login page


@app.route('/stats', subdomain="app", methods=['GET', 'POST'])
def beginst():
    if session.get('logged_in'):
        if session.get('role') == 'superadmin':
            return stat()
        elif session.get('role') == 'admin':
            return stat()
    else:
        return redirect("/")

@app.route('/stats/del', subdomain="app", methods=['GET', 'POST'])
def beginstatdel():
    if session.get('logged_in'):
        if session.get('role') == 'superadmin':
            return waitforrecdel()
        elif session.get('role') == 'admin':
            return waitforrecdel()
    else:
        return redirect("/")
    

@app.route('/stats/mod', subdomain="app", methods=['GET', 'POST'])
def beginstatdel1():
    if session.get('logged_in'):
        if session.get('role') == 'superadmin':
            return waitforrecdel()
        elif session.get('role') == 'admin':
            return waitforrecdel()
    else:
        return redirect("/")

@app.route('/gophishing', subdomain="app", methods=['GET', 'POST']) # main page route
def loginp():
    if session.get('logged_in'):
        if session.get('role') == 'superadmin':
            return gophish()
        elif session.get('role') == 'admin':
            return gophish()
    else:
        return redirect("/")

@app.route('/fy', subdomain="app", methods=['GET', 'POST']) # redirect to main if logged in
def logid():
    return apiid() # else redirect to login page

@app.route('/education/email', subdomain="app", methods=['GET', 'POST'])
def emaillobby():
    if session.get('logged_in'):
        return educationemaillobby()
    else:
        return redirect("/")

@app.route('/education/email/1', subdomain="app", methods=['GET', 'POST'])
def educationemail1():
    if session.get('logged_in'):
        return email1()
    else:
        return redirect("/")

@app.route('/education/email/2', subdomain="app", methods=['GET', 'POST'])
def educationemail2():
    if session.get('logged_in'):
        return email2()
    else:
        return redirect("/")

@app.route('/education/intro', subdomain="app", methods=['GET', 'POST'])
def educationintroload():
    if session.get('logged_in'):
        return educationintro()
    else:
        return redirect("/")

#### template iframe rendering for gophishing template preview
@app.route('/templates/amazon.html', subdomain="app", methods=['GET', 'POST']) 
def amazontemplate():
    if session.get('logged_in'):
        return render_template('amazon.html')
    else:
        return redirect('/')

@app.route('/templates/prototype2.html', subdomain="app", methods=['GET', 'POST']) 
def prototype2template():
    if session.get('logged_in'):
        return render_template('prototype2.html')
    else:
        return redirect('/')

@app.route('/templates/starbucks.html', subdomain="app", methods=['GET', 'POST']) 
def starbuckstemplate():
    if session.get('logged_in'):
        return render_template('starbucks.html')
    else:
        return redirect('/')
######################## end template render

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True #reload html templates when saved, while app is running
    app.run(host='0.0.0.0', debug=True)