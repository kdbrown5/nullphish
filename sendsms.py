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
from bitly import linkshorten

sendsms = Blueprint('sendsms', __name__, url_prefix='/sendsms', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

@sendsms.route('/sendsms', methods=['GET', 'POST'])

def sendtxt():
    def sendsmspost(smsrecipient, messagecontent):
        account_sid = "AC34370e6c0a300d0fd33641c804c9f510"
        auth_token  = "6494c074317d604b58cf07ec042c4f49"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=smsrecipient,
            from_="+18053211499",
            body=messagecontent)
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

    def queryuser():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from users where business = (?);', (business,))
        query = cur.fetchall()
        con.close()
        return query

    def querysingleuser(userpick):
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from users where username = (?) and business = (?);', (userpick, business,))
        query = cur.fetchall()
        con.close()
        return query

    def convertTuple(tup): 
        str =  ''.join(tup) 
        return str

    def lookupadmin():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select username from users where notify = 1 and business = (?);', (business,))
            admins = cur.fetchone()
            admins = admins[0]
        con.close
        return admins

    def scheduledb(username, phonedid, messagecontent, department, token, confirmation):
        print('sched')
        admins = lookupadmin()
        business = session['business']
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('insert into phishsched ( type, bitly, sentdate, scheduler, phonedid, username, business, message, admin, department, token, smsconfirmation) values ( "sms", 1, datetime("now", "localtime"), ?, ?, ?, ?, ?, ?, ?, ?, ? );', (session['username'], phonedid, username, business, messagecontent, admins, department, token, confirmation))
        con.close()

    #businessdata = businesslookup()
    userquery = queryuser()

    if request.method == 'POST':
        if 'userpick' in request.form:
            userpick = request.form.get('userpick')
            selecteduser = querysingleuser(userpick)
            userquery = queryuser()
            return render_template('sendsms.html', selecteduser=selecteduser, userquery=userquery) 

        phonenumber = request.form.get('phonenumber')
        print(phonenumber)
        if len(phonenumber) == 10:
            username = request.form.get('email')
            messagecontent = request.form.get('txtmessage')
            department = request.form.get('department')
            phonenumber = re.sub(r"\D", "", phonenumber)
            phonedid = phonenumber
            phonenumber = '1'+phonenumber
            phonenumber = int(phonenumber)
            receiveremail = request.form.get('email')
            newtoken = generate_confirmation_token(receiveremail)
            link = 'https://app.nullphish.com/fysms?id='+newtoken# +'&did='+(str(phonedid))
            link = linkshorten(link)
            link = link[0]
            messagecontent = messagecontent+' - '+link
            confirmation = sendsmspost(phonenumber, messagecontent)
            scheduledb(username, phonenumber, messagecontent, department, newtoken, confirmation)
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

    return render_template('sendsms.html', userquery=userquery)    
