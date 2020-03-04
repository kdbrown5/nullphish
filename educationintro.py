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

educationintro = Blueprint('educationintro', __name__, url_prefix='/education/intro', template_folder='templates')

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

@educationintro.route('/education/intro', subdomain="app", methods=['GET', 'POST']) 
def educationintro1():
    def lobby():
        print('educationintro')

    fname, lname = userlookup()
    timestamp = (datetime.now())
    timestamp = timestamp.strftime("%m/%d/%Y %I:%M")
    username=session['username']

    return render_template('educationintro.html')
