import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from lumberjack import log
from datetime import datetime

topic1 = Blueprint('topic1', __name__, url_prefix='/education/', template_folder='templates')

@topic1.route('/education/topic1', methods=['GET', 'POST']) ### url to keep modification / record deletion open
def topic11():

    def userlookup():
        con = sqlite3.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('select firstname from users where username = (?);', (session['username'],))
            fname = cur.fetchone()[0]
            cur.execute('select lastname from users where username = (?);', (session['username'],))
            lname = cur.fetchone()[0]
        con.close()
        return fname, lname

    fname, lname = userlookup()
    timestamp = (datetime.now())
    timestamp = timestamp.strftime("%m/%d/%Y %I:%M")
    username=session['username']

    return render_template('topic1mod1.html', fname=fname, lname=lname, username=username, timestamp=timestamp)