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

@educationemail.route('/education/topic1', methods=['GET', 'POST']) ### url to keep modification / record deletion open
def educationemaillobby():
    def selection():
        print('emaillobby')
    return render_template('emaillobby.html')