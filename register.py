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
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from tokenizer import generate_confirmation_token, confirm_token

db = SQLAlchemy()

register = Blueprint('register', __name__, url_prefix='/register', template_folder='templates')
@register.route("/register", methods=['GET', 'POST'])

def registration():
        
    def regsend(emailrecip, link, firstname):
        sender_email = "donotreply@nullphish.com"
        receiver_email = str(session['username'])
        password = "rtatstfu18as#R654"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome! Please complete registration"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        """

        changetemplate = open("templates/emailreg.html", "rt")###  read template and replace name 
        html = changetemplate.read()
        html = html.replace('username', firstname)
        html = html.replace('replacelink', link)
        changetemplate.close()

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first

        message.attach(part1)
        message.attach(part2)
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("webmail.nullphish.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

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
                cur.execute("INSERT INTO users (username, password, firstname, lastname, business, role, validated) VALUES (?, ?, ?, ?, ?, 'admin', 0);", (username, password, firstname, lastname, business,))
                cur.execute("INSERT INTO userperm (username, role, enroll, view, remove, email) VALUES (?, 'admin', 1, 1, 1, 1);", (username,))
                con.commit()
                con.close()
                gc.collect()
                session['role'] = 'admin'
                session['logged_in'] = True
                session['username'] = username
                emailrecip = username
                email = username
                newtoken = generate_confirmation_token(email)
                print(newtoken)
                link = 'http://localhost:5000/register?token='+newtoken
                regsend(emailrecip, link, firstname)
                flash('Success!  Please check your email for a confirmation link.')
                return render_template('register.html')

        if request.method == 'GET':
            if request.args.get('token'[:]) != None:
                try:
                    newtoken = request.args.get('token'[:])
                    email = confirm_token(newtoken)
                    if '@' in email:
                        con = sqlite3.connect('static/db1.db')
                        with con:
                            cur = con.cursor()
                            cur.execute('update users set validated = 1 where username = (?);', (email,))
                        con.close()
                        session['logged_in'] = True
                        return redirect('/profile')
                    else:
                        flash('The confirmation link is invalid or has expired (60 minutes)')
                        return render_template("register.html")
                except:
                    flash('The confirmation link is invalid or has expired (60 minutes)')
                    return render_template("register.html")
        return render_template("register.html")

    except Exception as e:
        return(str(e))

    return render_template("register.html")

