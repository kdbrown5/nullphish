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
        return completion

    def setrole(username):
        con = sqlite3.connect('static/db1.db')
        role = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT role FROM users where username = (?);", (username,))
            loadrole = cur.fetchall()
            loadrole = str(loadrole)
            loadrole = loadrole.replace(',', '')
            loadrole = loadrole.replace("'", '')
            loadrole = loadrole.replace('(', '')
            loadrole = loadrole.replace(')', '')
        return str(loadrole)

    def setbusiness(username):
        con = sqlite3.connect('static/db1.db')
        role = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT business FROM users where username = (?);", (username,))
            loadbusiness = cur.fetchall()
            loadbusiness = str(loadbusiness)
            loadbusiness = loadbusiness.replace(',', '')
            loadbusiness = loadbusiness.replace("'", '')
            loadbusiness = loadbusiness.replace('(', '')
            loadbusiness = loadbusiness.replace(')', '')
        return str(loadbusiness)

    error = None
    if request.method == 'POST':
        username = request.form.to_dict()['username']
        password = request.form.to_dict()['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = (username)
            session['logged_in'] = True
            role = setrole(username)
            session['role'] = str(role)
            business = setbusiness(username)
            session['business'] = str(business)
            return redirect('/')

    return render_template("login.html", error=error)







