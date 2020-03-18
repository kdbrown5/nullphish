import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from lumberjack import log
from maily import sendphish, customsendphish
from tokenizer import generate_confirmation_token, confirm_token
from pysqlcipher3 import dbapi2 as sqlite
import re
import twilio
from twilio.rest import Client

sendsms = Blueprint('sendsms', __name__, url_prefix='/sendsms', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

@sendsms.route('/sendsms', methods=['GET', 'POST'])

def sendtxt():
    def sendsmspost(smsrecipient):
        account_sid = "AC34370e6c0a300d0fd33641c804c9f510"
        auth_token  = "6494c074317d604b58cf07ec042c4f49"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=1+smsrecipient,
            from_="+18053211499",
            body="Hello from Python!")
        confirmation = message.sid
        return confirmation

    def businesslookup():
        con = sqlite.connect('db/db1.db')
        business = str(session['business'])
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            businessquery = []
            for row in cur.execute('select * from users where business LIKE (?);', (business,)):
                businessquery.append(row[:])
        con.close()
        businessdata = businessquery
        return businessdata

    def convertTuple(tup): 
        str =  ''.join(tup) 
        return str

    businessdata = businesslookup()

    if request.method == 'POST':
        phonenumber = request.form.get('phonenumber')
        print(phonenumber)
        if len(phonenumber) == 10:
            phonenumber = re.sub(r"\D", "", phonenumber)
            print(phonenumber)
            phonenumber = int(phonenumber)
            print(phonenumber)
            confirmation = sendsmspost(phonenumber)
            flash('Sent! - confirmation '+confirmation, 'category2')

            #receiveremail = request.form.get('email')
            #newtoken = generate_confirmation_token(receiveremail)
            #link = 'https://app.nullphish.com/fy?id='+newtoken
            #firstname = request.form.get('firstname')
            #lastname = request.form.get('lastname')
            #customsendphish(smtpserver, inserttemplate, receiveremail, firstname, lastname, subject, link, mailservbusiness)
            #flash('Email sent to: '+receiveremail, 'category2')
        else:
            flash('Not a valid number - format 8051113333', 'category2')

    return render_template('sendsms.html', businessdata=businessdata)    
