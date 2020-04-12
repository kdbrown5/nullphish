import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from lumberjack import log
from maily import sendphish, customsendphish
from tokenizer import generate_confirmation_token, confirm_token
from pysqlcipher3 import dbapi2 as sqlite
from bitly import linkshorten
from datetime import datetime

scheduled = Blueprint('scheduled', __name__, url_prefix='/scheduled', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

@scheduled.route('/scheduled', methods=['GET', 'POST'])
def viewschedule():
    def getschedule():
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from phishsched where business = (?) and sentdate = "none";', (session['business'],),)
        result = cur.fetchall()
        try:
            con.close()
        except:
            pass
        return result

    scheduleddata = getschedule()
    print(scheduleddata)
    for i in scheduleddata:
        for x in i:
            print(x)
    
    if request.method == 'POST':
        getfirstname = request.form.to_dict(flat=False)['firstname']
        getlastname = request.form.to_dict(flat=False)['lastname']
        getemail = request.form.to_dict(flat=False)['email']
        getdate = request.form.to_dict(flat=False)['datetimepicker']
        gettemplates = request.form.to_dict(flat=False)['templates']
        getselect = request.form.to_dict(flat=False)['select']
        getserver = request.form.to_dict(flat=False)['smtpserver']
        getbitly = request.form.to_dict(flat=False)['bitly']

    return render_template('scheduled.html', scheduleddata=scheduleddata)    
