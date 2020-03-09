import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from lumberjack import log
from pysqlcipher3 import dbapi2 as sqlite

phishingstats = Blueprint('phishingstats', __name__, url_prefix='/phishingstats', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

@phishingstats.route('/phishingstats', methods=['GET', 'POST']) ### url to keep modification / record deletion open
def phishingstatsload():
    def phishedlookup():
        con = sqlite.connect('db/db1.db')
        business = str(session['business'])
        business = business.replace('[', '')
        business = business.replace(']', '')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            businessquery = []
            for row in cur.execute('select * from phished where business LIKE (?)', (business,)):## populate tables with user data from same business
                businessquery.append(row[:])
        con.close()
        phishedquery = businessquery
        return phishedquery
        
    phishdata = phishedlookup()# return userdata list to render on page


    return render_template('phishingstats.html', phishdata=phishdata)   