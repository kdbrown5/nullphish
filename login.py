import requests
import sqlalchemy
import hashlib
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
import gc
from lumberjack import log
from pysqlcipher3 import dbapi2 as sqlite
from passlib.hash import argon2

db = SQLAlchemy()

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

login = Blueprint('login', __name__, url_prefix='/login', template_folder='templates')
@login.route("/login", subdomain='app', methods=['GET', 'POST'])

def loginpage():

    def check_password(hashed_password, user_password): # currently md5, will change to sha256 later
        password_check = argon2.verify(hashed_password, user_password)
        return password_check

    def validate(username, password): # validate username, pw from database
        con = sqlite.connect('db/db1.db')
        completion = False
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            for row in rows:
                dbUser = row[1]
                dbPass = row[2]
                if dbUser == username:
                    completion = check_password(password, dbPass)
            cur.execute('select validated from users where username = (?)', (username,))
            validated = cur.fetchone()[0]
            session['validated'] = validated
        con.close()
        return completion

    def setrole(username):
        con = sqlite.connect('db/db1.db')
        role = None
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute("SELECT role FROM users where username = (?);", (username,))
            loadrole = cur.fetchone()
            loadrole = str(loadrole[0])
        con.close()
        return loadrole

    def setbusiness(username):
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute("SELECT business FROM users where username = (?);", (username,))
            loadbusiness = cur.fetchone()
            loadbusiness = str(loadbusiness[0])
        con.close()
        return loadbusiness

    def reguserlookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            con.row_factory = sqlite.Row
            cur.execute('select firstname, lastname, department, role from users where business = (?);', (session['business'],))
            reguserquery = cur.fetchall()
        con.close()
        return reguserquery

    error = None


    if request.method == 'POST':
        if session['authemulate'] == True:
            print(request.form('emulateuser'))
            emulateuserrequest = request.form('emulateuser')
            session['username'] = emulateuserrequest
            return redirect ('/profile')
        username = request.form.to_dict()['username']
        password = request.form.to_dict()['password']
        completion = validate(username, password)
        if session['validated'] == 0:
            error = 'It looks like your account is not yet activated. Please contact your administrator'
        elif session['validated'] == 2:
            error = 'It looks like your account has been suspended.  Please contact your administrator'
        elif completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = (username)
            session['logged_in'] = True
            role = setrole(username)
            session['role'] = role
            business = setbusiness(username)
            session['business'] = business
            if role == 'superadmin':
                session['authemulate'] = True
                userlist = reguserlookup()
                return render_template('emulatelogin.html', userlist=userlist)
            session['authemulate'] = False
            return redirect('/')



    return render_template("login.html", error=error)