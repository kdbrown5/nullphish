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
from flask_mail import Mail, Message

db = SQLAlchemy()

register = Blueprint('register', __name__, url_prefix='/register', template_folder='templates')
@register.route("/register", methods=['GET', 'POST'])

def registration():
    def regsend(emailrecip, link, firstname):
        app = Flask(__name__)
        app.config.update(
            DEBUG=True,
            #EMAIL SETTINGS
            MAIL_SERVER='webmail.nullphish.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME = 'donotreply@nullphish.com',
            MAIL_PASSWORD = 'rtatstfu18as#R654'
            )
        mail = Mail(app)
        emailrecip=str(session['username'])
        link='https://google.com'

        msg = Message("Welcome! Please Complete Registration",
        sender="donotreply@nullphish.com",
        recipients=[emailrecip])
        with app.app_context():
            msg.body = 'Hello,+\n Please follow this link to complete registration for Nullphish.com:'+link+session['username']
            msg.html=render_template('emailreg.html', firstname=firstname)
            mail.send(msg)
    
    
    try:
        if request.method == "POST":
            firstname = request.form.to_dict()['firstname']
            lastname = request.form.to_dict()['lastname']
            username = request.form.to_dict()['email']
            business = request.form.to_dict()['business']
            session['username'] = username
            #password = sha256_crypt.encrypt((str(request.form.get('password'))))
            password = request.form.get('password')
            if len(password) < 10:
                flash('Please use a password with at least 10 characters')
                return render_template("register.html")

            password = hashlib.md5(str(request.form.get('password')).encode()).hexdigest()
            repeat = hashlib.md5(str(request.form.get('repeat')).encode()).hexdigest()
            code = request.form.to_dict()['code']
            if repeat != password:
                flash('Your passwords do not match.  Please try again.')
                return render_template("register.html")
            con = sqlite3.connect('static/db1.db')

            if code != 'goat':
                if code != 'kdb':
                    flash('Incorrect registration code')
                    return render_template("register.html")
                else:
                    pass
            

            with con:
                cur = con.cursor()
                x = cur.execute("SELECT * FROM users WHERE username LIKE (?);", (session['username'],))
            result = cur.fetchone()

            if result == None:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, password, firstname, lastname, business, role) VALUES (?, ?, ?, ?, ?, 'admin');", (username, password, firstname, lastname, business,))
                cur.execute("INSERT INTO userperm (username, role, enroll, view, remove, email) VALUES (?, 'admin', 1, 1, 1, 1);", (username,))
                con.commit()
                con.close()
                gc.collect()
                session['role'] = 'admin'
                session['logged_in'] = True
                session['username'] = username
                emailrecip = username
                link = 'https://gokdb.com/'
                regsend(emailrecip, link, firstname)
                return redirect('/profile')


            if result != None:
                flash("An account with that email address is taken, please choose another")
                return render_template('register.html')

        return render_template("register.html")

    except Exception as e:
        return(str(e))
    
    return render_template("register.html")










    
