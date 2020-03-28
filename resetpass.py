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

    def lookupfirstname(username):
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select firstname from users where username = (?);', username)
            if cur.fetchone():
                validusername = cur.fetchone()
            else:
                validusername = False
            return validusername

    def userlookup(username):
        con = sqlite.connect('db/db1.db')
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
            emulatebusiness = cur.fecthone()
            emulatebusiness = emulatebusiness[0]
        con.close()
        return emulatefname, emulatelname, emulatedept, emulaterole, emulatebusiness   

    def sendreset(firstname, emailrecip, link):
        sender_email = "donotreply@nullphish.com"
        receiver_email = emailrecip
        emailrecip = str(emailrecip)
        firstname = str(firstname)

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
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("webmail.nullphish.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    if request.method == 'GET':
        usertoken = (processtoken())
        email = str(confirm_15mtoken(usertoken))
        timestamp = (datetime.now())
        timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
        timestamp = timestamp.replace(' ', '-')
        if '@' in email:
            session['fname'], session['lname'], session['department'], session['role'], session['business'] = userlookup(email)
            session['username'] = email
            session['validated'] = 1
            session['logged_in'] = True
            return redirect('/profile')

    if request.method == 'POST':
        username = request.form.to_dict()['username']
        if '@' in username:
            username = [username]
            validusername = checkuser(username)
            if validusername != False:
                newtoken = generate_confirmation_token(username)
                link = 'https://app.nullphish.com/resetpass?token='+newtoken
                firstname = lookupfirstname(username)
                sendreset(firstname, username, link)
                flash('Invitation Email sent to: '+emailrecip+'!', 'category2')


    return render_template('resetpassform.html')