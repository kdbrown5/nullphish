import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from pysqlcipher3 import dbapi2 as sqlite
from lumberjack import log
from datetime import datetime

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

educationemail = Blueprint('educationemail', __name__, url_prefix='/education/email', template_folder='templates')

@educationemail.route('/education/email', methods=['GET', 'POST']) 
def educationemaillobby():
    def selection():
        print('emaillobby')

    return render_template('emaillobby.html')

@educationemail.route('/education/email/1', subdomain="app", methods=['GET', 'POST'])
def email1():
    def userlookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select firstname from users where username = (?);', (session['username'],))
            fname = cur.fetchone()[0]
            cur.execute('select lastname from users where username = (?);', (session['username'],))
            lname = cur.fetchone()[0]
        con.close()
        return fname, lname

    def trackpage():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('UPDATE email set visited = visited +1 where username = (?) and pagenum = 1;', (session['username'],))
            cur.execute('insert into email (username, pagenum, visited) select (?), 1, 1 where (Select changes() = 0);', (session['username'],))
        con.close()

    fname, lname = userlookup()
    timestamp = (datetime.now())
    timestamp = timestamp.strftime("%m/%d/%Y %I:%M")
    username=session['username']
    trackpage()

    if request.method == 'GET':
        if request.args.get('!'[:]) == None:
            pass
        else:
            flash('Never click links! You could have been sent to a malicious website!', 'category2')
            return render_template('email1.html', fname=fname, lname=lname, username=username, timestamp=timestamp)

    return render_template('email1.html', fname=fname, lname=lname, username=username, timestamp=timestamp)

#@educationemail.route('/education/email/2', subdomain="app", methods=['GET', 'POST'])