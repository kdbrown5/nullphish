import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from lumberjack import log
from pysqlcipher3 import dbapi2 as sqlite
from io import StringIO
from werkzeug.wrappers import Response
import csv

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
        
    def download_report():
        def generate():
            data = StringIO()
            w = csv.writer(data)# write header
            w.writerow(('Department', 'Method', 'User Phished', 'Business', 'Admin Notified', 'Date'))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)# write each log item
            print(emailquery)
            for item in emailquery:
                w.writerow((
                    item[7],
                    item[10],
                    item[1],
                    item[4],
                    item[6],
                    item[3].isoformat()  # format datetime as string
                ))
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)# stream the response as the data is generated
        response = Response(generate(), mimetype='text/csv') # add a filename
        response.headers.set("Content-Disposition", "attachment", filename="report.csv")
        return response

    def export():
        si = StringIO()
        cw = csv.writer(si)
        for item in emailquery:
            cw.writerow((
                item[7],
                item[10],
                item[1],
                item[4],
                item[6],
                item[3].isoformat()  # format datetime as string
            ))
        response = make_response(si.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=report.csv'
        response.headers["Content-type"] = "text/csv"
        return response

    emailquery, smsquery = phishedlookup()# return userdata list to render on page
    export()

    return render_template('phishingstats.html', emailquery=emailquery, smsquery=smsquery)   