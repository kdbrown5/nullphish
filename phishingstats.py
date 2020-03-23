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
        
    def exportemail(newreport):
        with open(newreport, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Department', 'Method', 'User_Phished', 'Business', 'Admin_Notified', 'Date'))
            for item in emailquery:
                writer.writerow((item[7], item[10], item[1], item[4], item[6], item[3]))

    def exportsms(newreport):
        with open(newreport, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Department', 'Method', 'User_Phished', 'Phone_Number', 'Business', 'Admin_Notified', 'Date'))
            for item in smsquery:
                writer.writerow((item[7], item[10], item[1], item[12], item[4], item[6], item[3]))

    emailquery, smsquery = phishedlookup()# return userdata list to render on page

    if request.method == "POST":
        if request.form.get('report') == "E-Mail Report" or "E-MAIL":
            businessdir = './reports/businesses/'+session['business']
            if not os.path.exists(businessdir):
                os.makedirs(businessdir)
            #Path("./reports/businesses/"+str(session['business'])).mkdir(parents=True, exist_ok=True)
            newreport = 'reports/businesses/'+session['business']+'/emailreport.csv'
            exportemail(newreport)
            return send_file(newreport, as_attachment=True, attachment_filename='emailreport.csv')

        if request.form.get('report') == "SMS" or "SMS Report":
            businessdir = './reports/businesses/'+session['business']
            if not os.path.exists(businessdir):
                os.makedirs(businessdir)
            #Path("./reports/businesses/"+str(session['business'])).mkdir(parents=True, exist_ok=True)
            newreport = 'reports/businesses/'+session['business']+'/smsreport.csv'
            exportsms(newreport)
            return send_file(newreport, as_attachment=True, attachment_filename='smsreport.csv')

    return render_template('phishingstats.html', emailquery=emailquery, smsquery=smsquery)   