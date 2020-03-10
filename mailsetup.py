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
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select mailhost, mailuser, mailtype, mailport from mailconfig where business = (?);', (session['business'],))
            currentsetup = cur.fetchall()
            return currentsetup
        
    currentsetup = lookupcurrentsettings()
                
    if request.method == 'POST':
        if session['logged_in'] == True:
            if 'mailhost' in request.form:
                mailhost = request.form['mailhost']
                mailuser = request.form['mailuser']
                mailpass = request.form['mailpass']
                mailtype = request.form['mailtype']
                mailport = request.form['mailport']
                timestamp = (datetime.now())
                timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
                timestamp = timestamp.replace(' ', '-')
                con = sqlite.connect('db/db1.db')
                with con:
                    cur = con.cursor()
                    cur.execute('PRAGMA key = '+dbkey+';')
                    cur.execute('insert into mailconfig (mailhost, mailuser, mailpass, mailtype, mailport, business, date) values ((?), (?), (?), (?), (?), (?), (?));', (mailhost, mailuser, mailpass, mailport, mailport, session['business'], timestamp,))
                con.close()
                flash('Mail server added!', 'category2')
                return return_render('mailsetup.html')
            else:
                pass
        else:
            return redirect('/')
    else:
        return render_template('mailsetup.html', currentsetup=currentsetup)

    return render_template('mailsetup.html', currentsetup=currentsetup)