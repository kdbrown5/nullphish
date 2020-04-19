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
from datetime import datetime

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
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from phishsched where activetime != "none" and business = (?) and type = "email";', (session['business'],),)
        emailquery = cur.fetchall()
        cur.execute('select * from phishsched where activetime != "none" and business = (?) and type = "sms";', (session['business'],),)
        smsquery = cur.fetchall()      
            #for row in cur.execute('select * from phishsched where business LIKE (?) and method = "SMS";', (business,)):## populate tables with user data from same business
            #    smsquery.append(row[:])            
        con.close()
        return emailquery, smsquery

    def emaillookup():
        con = sqlite.connect('db/db1.db')
        business = str(session['business'])
        business = business.replace('[', '')
        business = business.replace(']', '')
        con = sqlite.connect('db/db1.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from phishsched where activetime != "none" and business = (?) and type = "email";', (session['business'],),)
        emaildict = cur.fetchall()
            #for row in cur.execute('select * from phishsched where business LIKE (?) and method = "SMS";', (business,)):## populate tables with user data from same business
            #    smsquery.append(row[:])            
        con.close()
        return emaildict

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d       

    def exportemail(newreport):
        with open(newreport, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Business','Department', 'Method', 'User_Phished', 'Template_Used', 'Hyperlink', 'Sender_Email', 'Scheduler', 'Admin_Notified', 'Date_Sent', 'Date_Read'))
            emailstats = emaillookup()
            for item in emailstats:
                writer.writerow(item.get('business'), item.get('department'), item.get('username'))
                #writer.writerow((item.business, item.department, item.type, item.username, item.template, item.bitly, item.mailname, item.scheduler, item.admin, item.sentdate, item.activetime))

    def exportsms(newreport):
        with open(newreport, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Department', 'Method', 'User_Phished', 'Phone_Number', 'Business', 'Admin_Notified', 'Date'))
            for item in smsquery:
                print(item)
                #writer.writerow((item[7], item[10], item[1], item[12], item[4], item[6], item[3]))

    emailquery, smsquery = phishedlookup()# return userdata list to render on page

    if request.method == "POST":
        if request.form.get('report') == "E-Mail Report":
            businessdir = './reports/businesses/'+session['business']
            if not os.path.exists(businessdir):
                os.makedirs(businessdir)
            newreport = 'reports/businesses/'+session['business']+'/emailreport.csv'
            exportemail(newreport)
            datestamp = datetime.now().strftime('%m-%d-%Y_%I-%M%p')
            return send_file(newreport, as_attachment=True, attachment_filename='emailreport-'+datestamp+'.csv')

        if request.form.get('report') == "SMS Report":
            businessdir = './reports/businesses/'+session['business']
            if not os.path.exists(businessdir):
                os.makedirs(businessdir)
            newreport = 'reports/businesses/'+session['business']+'/smsreport.csv'
            exportsms(newreport)
            datestamp = datetime.now().strftime('%m-%d-%Y_%I-%M%p')
            return send_file(newreport, as_attachment=True, attachment_filename='smsreport-'+datestamp+'.csv')

    return render_template('phishingstats.html', emailquery=emailquery, smsquery=smsquery)   