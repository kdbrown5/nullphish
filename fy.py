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
from tokenizer import generate_confirmation_token, confirm_twoweektoken
from datetime import datetime
from pysqlcipher3 import dbapi2 as sqlite

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

db = SQLAlchemy()
fy = Blueprint('fy', __name__, url_prefix='/fy', template_folder='templates')
@fy.route("/fy", methods=['GET', 'POST'])

def apiid():
    def tattletale(emailrecip, email):
        sender_email = "donotreply@nullphish.com"
        receiver_email = emailrecip
        password = "rtatstfu18as#R654"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "One of your team members has been Phished!"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        """

        changetemplate = open("templates/tattle.html", "rt")###  read template and replace name 
        html = changetemplate.read()
        html = html.replace('replaceusername', email)
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


    def processtoken():
        if request.method == 'GET':
            if request.args.get('id'[:]) != None:
                usertoken = request.args.get('id')
                return usertoken
                
    if request.method == 'GET':
        usertoken = (processtoken())
        email = str(confirm_twoweektoken(usertoken))
        timestamp = (datetime.now())
        timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
        timestamp = timestamp.replace(' ', '-')
        if '@' in email:
            con = sqlite.connect('db/db1.db')
            with con:
                cur = con.cursor()
                cur.execute('PRAGMA key = '+dbkey+';')
                cur.execute('insert into phished (username, date) values ((?), (?));', (email, timestamp))
                cur.execute('select business from users where username = (?);', (email,))
                business = cur.fetchone()[0]
                cur.execute('select username from users where role = "admin" and business = (?);', (business,))
                admins = cur.fetchall()
            con.close()
            adminlist = []
            for row in admins:
                row = str(row)
                row = row[2:-3]
                adminlist.append(row)
            emailrecip = adminlist[0]
            tattletale(emailrecip, email)
            return redirect('https://nullphish.com')
        else:
            return redirect('https://nullphish.com')


        
    return redirect('https://nullphish.com')