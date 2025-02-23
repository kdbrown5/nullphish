import requests
import sqlalchemy
import hashlib
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from lumberjack import log
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tokenizer import generate_confirmation_token, confirm_15mtoken   
from datetime import datetime
from pysqlcipher3 import dbapi2 as sqlite
import urllib3
from urllib.request import urlopen


loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

resetpass = Blueprint('resetpass', __name__, url_prefix='/resetpass', template_folder='templates')
@resetpass.route("/resetpass", subdomain='app', methods=['GET', 'POST'])

def doresetpass():
    def processtoken():
        if request.method == 'GET':
            if request.args.get('id'[:]) != None:
                usertoken = request.args.get('id')
                return usertoken

    def checkuser(username):
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select username from users where username = (?);', username)
            if cur.fetchone():
                validusername = cur.fetchone()
            else:
                validusername = False
            return validusername

    def logpwreset(username):
        timestamp = (datetime.now())
        timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
        timestamp = timestamp.replace(' ', '-')
        print(timestamp)
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('insert into passreset (username, date) values ((?), (?));', (username, timestamp))
        con.close()

    def lookupfirstname(username):
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select firstname from users where username = (?);', username)
            try:
                validusername = cur.fetchone()
                return validusername
            except:
                validusername = False
                return validusername

    def userlookup(username):
        con = sqlite.connect('db/db1.db')
        username = username
        username = username.replace("['", '')
        username = username.replace("']", '')
        username = [username]
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select firstname from users where username = (?);', (username))
            emulatefname = cur.fetchone()
            emulatefname = emulatefname[0]
            cur.execute('select lastname from users where username = (?);', (username))
            emulatelname = cur.fetchone()
            emulatelname = emulatelname[0]
            cur.execute('select department from users where username = (?);', (username))
            emulatedept = cur.fetchone()
            emulatedept = emulatedept[0]
            cur.execute('select role from users where username = (?);', (username))
            emulaterole = cur.fetchone()
            emulaterole = emulaterole[0]
            cur.execute('select business from users where username = (?);', (username))
            emulatebusiness = cur.fetchone()
            emulatebusiness = emulatebusiness[0]
        con.close()
        return emulatefname, emulatelname, emulatedept, emulaterole, emulatebusiness   

    def sendreset(firstname, emailrecip, link):
        sender_email = "donotreply@nullphish.com"
        emailrecip = str(emailrecip)
        emailrecip = emailrecip.replace("['", '')
        emailrecip = emailrecip.replace("']", '')
        receiver_email = emailrecip
        firstname = str(firstname)
        firstname = firstname.replace("('", '')
        firstname = firstname.replace("',)", '')
        link = str(link)

        print('send to: '+receiver_email)

        password = "rtatstfu18as#R654"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset - NullPhish"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        """

        changetemplate = open("templates/resetpassemail.html", "rt")###  read template and replace name 
        html = changetemplate.read()
        html = html.replace('receiveremail', emailrecip)
        html = html.replace('firstname', firstname)
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
        context = ssl._create_unverified_context()
        
        with smtplib.SMTP_SSL("webmail.nullphish.com", 465, context=ssl._create_unverified_context()) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    if request.method == 'GET':
        if request.args.get('id'[:]) == None:
            return render_template('resetpassform.html')
        else:
            usertoken = (processtoken())
            email = str(confirm_15mtoken(usertoken))
            if '@' in email:
                timestamp = (datetime.now())
                timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
                timestamp = timestamp.replace(' ', '-')
                emulatefname, emulatelname, emulatedept, emulaterole, emulatebusiness = userlookup(email)
                session['fname'] = emulatefname
                session['lname'] = emulatelname
                session['department'] = emulatedept
                session['role'] = emulaterole
                session['business'] = emulatebusiness
                email = email.replace("['", '')
                email = email.replace("']", '')
                email = [email]
                email = email[0]
                logpwreset(email)
                session['username'] = email
                session['validated'] = 1
                session['logged_in'] = True
                return redirect('/profile')
            else:
                flash('Not a valid user, or token has expired', 'category2')
                return render_template('resetpassform.html')

    if request.method == 'POST':
        username = request.form.to_dict()['username']
        if '@' in username:
            username = [username]
            validusername = checkuser(username)
            if validusername != False:
                newtoken = generate_confirmation_token(username)
                link = 'https://app.nullphish.com/resetpass?id='+newtoken
                firstname = lookupfirstname(username)
                sendreset(firstname, username, link)
                flash('Reset sent!  Check your inbox for reset link', 'category2')
                return render_template('resetpassform.html')


    return render_template('resetpassform.html')