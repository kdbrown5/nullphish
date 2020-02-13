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
    def topic1mod1():
        print('placeholder')
        

    topic1mod1()
    fname=session['fname']
    lname=session['lname']
    timestamp = (datetime.now())
    timestamp = timestamp.strftime("%m/%d/%Y %I:%M")
    username=session['username']

    return render_template('topic1mod1.html', fname=fname, lname=lname, username=username, timestamp=timestamp)