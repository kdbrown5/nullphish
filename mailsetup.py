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
from datetime import datetime
from pysqlcipher3 import dbapi2 as sqlite
import base64

### add table for config to the database - mailconfig
# - smtp server/host - # ex smtp.office365.com
# - mailbox username
# - mailbox pass
# - mail connector settings - NONE /  SSL /  TLS
# - ^ 25 / 465 / 587
# - business
# - modified date
#
# create table mailconfig ( id integer PRIMARY KEY autoincrement, mailhost text, mailuser text, mailpass text, mailtype text, mailport integer, business text, date text )


loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

mailsetup = Blueprint('mailsetup', __name__, url_prefix='/mailsetup', template_folder='templates')
@mailsetup.route("/mailsetup", methods=['GET', 'POST'])

def mailconfig():
    def lookupcurrentsettings():
        con = sqlite.connect('db/db1.db')
        with con:
            currentsetup = []
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select name, mailhost, mailuser, mailtype, mailport from mailconfig where business = (?);', (session['business'],))
            for mailname, mailhost, mailuser, mailtype, mailport in cur.fetchall():
                currentsetup.append(Markup('<strong> Name:</strong>&nbsp;'+mailname))
                currentsetup.append(Markup('<strong> Mail Server:</strong>&nbsp;'+mailhost))
                currentsetup.append(Markup('<strong> Mail Username:</strong>&nbsp;'+mailuser))
                currentsetup.append(Markup('<strong> Protocol:</strong>&nbsp;'+mailtype))
                currentsetup.append(Markup('<strong> Port:</strong>&nbsp;'+str(mailport)))
            return currentsetup

    def bencode(mailpass):
        makeutf=mailpass.encode("utf-8")
        encoded = base64.b64encode(makeutf)
        return encoded

    currentsetup = lookupcurrentsettings()
                
    if request.method == 'POST':
        if session['logged_in'] == True:
            if 'submit' in request.form:
                try:
                    mailname = request.form['mailname']
                    mailname = mailname.replace(' ', '_')
                    mailhost = request.form['mailhost']
                    mailuser = request.form['mailuser']
                    temppass = request.form['mailpass']
                    mailpass = bencode(temppass)
                    mailtype = request.form['mailtype']
                    mailport = request.form['mailport']
                    timestamp = (datetime.now())
                    timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
                    timestamp = timestamp.replace(' ', '-')
                    con = sqlite.connect('db/db1.db')
                    with con:
                        cur = con.cursor()
                        cur.execute('PRAGMA key = '+dbkey+';')
                        cur.execute('update mailconfig set mailhost = (?), mailuser = (?), mailpass = (?), mailtype = (?), mailport = (?), name = (?), date = (?) where business = (?);', (mailhost, mailuser, mailpass, mailtype, mailport, mailname, timestamp, session['business'],))
                        cur.execute('insert or ignore into mailconfig (mailhost, mailuser, mailpass, mailtype, mailport, business, name, date) values ((?), (?), (?), (?), (?), (?), (?), (?));', (mailhost, mailuser, mailpass, mailtype, mailport, session['business'], mailname, timestamp,))
                    con.close()
                    flash('Mail server added!', 'category2')
                    return render_template('mailsetup.html')
                except:
                    flash('Please fill out all fields', 'category2')
                    return render_template('mailsetup.html')
            else:
                pass
        else:
            return redirect('/')
    else:
        return render_template('mailsetup.html', currentsetup=currentsetup)

    return render_template('mailsetup.html', currentsetup=currentsetup)