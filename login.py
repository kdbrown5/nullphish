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
import sqlite3
from lumberjack import log

db = SQLAlchemy()

login = Blueprint('login', __name__, url_prefix='/login', template_folder='templates')
@login.route("/login", methods=['GET', 'POST'])

def loginpage():

    def check_password(hashed_password, user_password): # currently md5, will change to sha256 later
        return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

    def validate(username, password): # validate username, pw from database
        con = sqlite3.connect('static/db1.db')
        completion = False
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            for row in rows:
                dbUser = row[1]
                dbPass = row[2]
                if dbUser == username:
                    completion = check_password(dbPass, password)
            cur.execute('select validated from users where username = (?)', (username,))
            validated = cur.fetchone()[0]
            session['validated'] = validated
        con.close()
        return completion

    def setrole(username):
        con = sqlite3.connect('static/db1.db')
        role = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT role FROM users where username = (?);", (username,))
            loadrole = cur.fetchone()
            loadrole = str(loadrole[0])
        con.close()
        return loadrole

    def setbusiness(username):
        con = sqlite3.connect('static/db1.db')
        role = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT business FROM users where username = (?);", (username,))
            loadbusiness = cur.fetchone()
            loadbusiness = str(loadbusiness[0])
        con.close()
        return loadbusiness

    error = None
    if request.method == 'POST':
        username = request.form.to_dict()['username']
        password = request.form.to_dict()['password']
        completion = validate(username, password)
        print(session['validated'])
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
            return redirect('/')

    return render_template("login.html", error=error)