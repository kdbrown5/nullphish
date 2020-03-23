import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from lumberjack import log
from pysqlcipher3 import dbapi2 as sqlite
#from io import StringIO
#from werkzeug.wrappers import Response
import csv
import os.path
from pathlib import Path

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
            emailquery = []
            for row in cur.execute('select * from phished where business LIKE (?) and method = "E-MAIL";', (business,)):## populate tables with user data from same business
                emailquery.append(row[:])
            smsquery = []
            for row in cur.execute('select * from phished where business LIKE (?) and method = "SMS";', (business,)):## populate tables with user data from same business
                smsquery.append(row[:])            
        con.close()
        return emailquery, smsquery
        
    def export():
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(emailquery)    



    emailquery, smsquery = phishedlookup()# return userdata list to render on page
    businessdir = './reports/businesses/'+session['business']
    if not os.path.exists(businessdir):
        os.makedirs(businessdir)
    #Path("./reports/businesses/"+str(session['business'])).mkdir(parents=True, exist_ok=True)
    #newreport = './reports/businesses/'+session['business']+'/phishingreport.csv'
    export()

    return render_template('phishingstats.html', emailquery=emailquery, smsquery=smsquery)   