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
import urllib3
from urllib.request import urlopen

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

db = SQLAlchemy()
fysms = Blueprint('fysms', __name__, url_prefix='/fysms', template_folder='templates')
@fysms.route("/fysms", methods=['GET', 'POST'])

def smsapiid():
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
        context = ssl._create_unverified_context()
        
        with smtplib.SMTP_SSL("webmail.nullphish.com", 465, context=ssl._create_unverified_context()) as server:
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
        print('api test')
        print(request.args.get('id'))
        usertoken = (processtoken())
        email = str(confirm_twoweektoken(usertoken))
        #timestamp = (datetime.now())
        #timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
        #timestamp = timestamp.replace(' ', '-')
        if '@' in email:
            #phonedid = request.args.get('did')
            con = sqlite.connect('db/db1.db')
            with con:
                cur = con.cursor()
                cur.execute('PRAGMA key = '+dbkey+';')
                print('usertoken')
                print(usertoken)
                print(type(usertoken))
                cur.execute('update phishsched set activetime = DATETIME("now", "localtime") where token = (?) and activetime = "none" and sentdate < DATETIME("now", "localtime", "-10 seconds");', (usertoken,))
                #cur.execute('select id from phishsched where token = (?) and sentdate > DATETIME("now", "localtime", "-20 seconds");', (usertoken,))
                #getid = cur.fectchone()
                #print('getid')
                #print(getid)
                #cur.execute('update phishsched set activetime = DATETIME("now", "localtime") where type = "sms" and token = (?);', (usertoken,))
                cur.execute('select admin from phishsched where token = (?) and (select changes() = 1);', (usertoken,))
                try:
                    emailrecip = cur.fetchall()
                    emailrecip = emailrecip[0]
                    emailrecip = str(emailrecip)
                    emailrecip = emailrecip.replace("('", '')
                    emailrecip = emailrecip.replace("',)", '')
                    print('fysms emailrecip')
                    print(emailrecip)

                    sendtattle = True
                except:
                    print('no update made - no admin received')
                    sendtattle = False
                #cur.execute('update phishsched set activetime = DATETIME("now", "localtime") where id = (?);', (getid,))
                #
                #cur.execute('UPDATE phished set hit = hit +1 where token = (?) and username = (?);', (usertoken, email,))
                #cur.execute('UPDATE phished set phonedid = (?) where token = (?);', (phonedid, usertoken,))
                #cur.execute('select hit from phished where token = (?);', (usertoken,))
                #try:
                #    hitcount = cur.fetchone()[0]
                #    hitcount = int(hitcount)
                #except:
                #    hitcount = 0
                #if hitcount > 1:
                #    cur.execute('UPDATE phished set date = (?) where token = (?) and username = (?);', (timestamp, usertoken, email,))
                #    cur.execute('select business from users where username = (?);', (email,))
                #    business = cur.fetchone()[0]
                #    cur.execute('update phished set business = (?) where date = (?);', (business, timestamp,))
                #    cur.execute('select username from users where notify = 1 and business = (?);', (business,))
                #    admins = cur.fetchone()[0]
                #    cur.execute('update phished set admin = (?) where date = (?);', (admins, timestamp,))
                #    cur.execute('select department from users where username = (?);', (email,))
                #    userdept = cur.fetchone()[0]
                #    cur.execute('update phished set department = (?) where date = (?);', (userdept, timestamp,))
                #if hitcount == 0:
                #    cur.execute('insert into phished (username, token, method) values ((?), (?), "SMS");', (email, usertoken))
            con.close()
            #if hitcount > 1:
            #    emailrecip = admins
            if sendtattle == True:
                tattletale(emailrecip, email)
            return redirect('https://google.com')

        else:
            return redirect('https://google.com')


        
    return redirect('https://google.com')