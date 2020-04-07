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

schedulephish = Blueprint('schedulephish', __name__, url_prefix='/schedulephish', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

def checkschedule():
    con = sqlite.connect('db/db1.db')
    with con:
        emailsched = []
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        for row in cur.execute('select * from phishsched where type = "email" and date between "2020-04-01" and DATETIME("now", "localtime", "+5 minutes") and sentdate = "none";'):
            emailsched.append(row[:])
        for email in emailsched:
            timestamp = (datetime.now())
            timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
            timestamp = timestamp.replace(' ', '-')
            zid = email[0]
            #ztype = email[1]
            zemail = email[2]
            zemail = [zemail]
            zemail = zemail[0]
            ztemplate = email[3]
            zsender = email[4]
            zsender = convertTuple(zsender)
            #zdate = email[5]
            zbitly = email[6]
            zbusiness = email[7]
            zbusiness = [zbusiness]
            zbusiness = zbusiness[0]
            ztemplate = '/home/nullphish/prod/templates/businesses/'+zbusiness+'/'+ztemplate+'.html'
            zsubject = email[8]
            cur.execute('select firstname from users where username = (?);', (zemail,))
            zfirstname = cur.fetchall()
            zfirstname = str(zfirstname[0])
            zfirstname = zfirstname.replace("('", '')
            zfirstname = zfirstname.replace("',)", '')
            cur.execute('select lastname from users where username = (?);', (zemail,))
            zlastname = cur.fetchall()
            zlastname = str(zlastname[0])
            zlastname = zlastname.replace("('", '')
            zlastname = zlastname.replace("',)", '')
            ztoken = generate_confirmation_token(zemail)
            timestamp = [timestamp]
            timestamp = convertTuple(timestamp[0])
            if zbitly == 1:
                zlink = 'https://app.nullphish.com/fy?id='+ztoken+'&template='+(str(ztemplate))
                zlink = linkshorten(zlink)
                zlink = [zlink]
                zlink = zlink[0]
                customsendphish(zsender, ztemplate, zemail, zfirstname, zlastname, zsubject, zlink, zbusiness)
                cur.execute('update phishsched set sentdate = (datetime("now", "localtime")) where id = (?);', (zid,))
            else:
                zlink = 'https://app.nullphish.com/fy?id='+ztoken+'&template='+(str(ztemplate))
                zlink = [zlink]
                customsendphish(zsender, ztemplate, zemail, zfirstname, zlastname, zsubject, zlink, zbusiness)
                cur.execute('update phishsched set sentdate = (datetime("now", "localtime")) where id = (?);', (zid,))     

@schedulephish.route('/schedulephish', methods=['GET', 'POST'])
def phishschedule():
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

    def lookupmailserver():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            serverlist = []
            for row in cur.execute('select name from mailconfig where business = (?) OR share = 1;', (business,)):
                serverlist.append(row[:][0])
        con.close()
        return serverlist

    def lookuptemplates():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            templatelist = []
            for row in cur.execute('select name from templates where business = (?) or shared = 1;', (business,)):
                templatelist.append(row[:][0])
            con.close
        return templatelist

    def convertTuple(tup): 
        str =  ''.join(tup) 
        return str

    def lookupemailsubject(templatename):
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select emailsubject from templates where business LIKE (?) and name LIKE (?);', (business, templatename,))
            emailsubject = cur.fetchall()[0]
        con.close
        emailsubject = convertTuple(emailsubject)
        return emailsubject

    availtemplates = lookuptemplates()
    businessdata = businesslookup()
    serverlist = lookupmailserver()

    if request.method == 'POST':
        print(request.form)
        print(request.form.get('datetimepicker'))
        if 0 == 1:
            mailservbusiness = session['business']              
            subject = lookupemailsubject(templatename)
            receiveremail = request.form.get('email')
            newtoken = generate_confirmation_token(receiveremail)
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            if request.form.get('shorten') == 'bitly':  
                link = 'https://app.nullphish.com/fy?id='+newtoken+'&template='+(str(templatename))
                link = linkshorten(link)
                customsendphish(smtpserver, inserttemplate, receiveremail, firstname, lastname, subject, link, mailservbusiness)
                flash('Email sent to: '+receiveremail, 'category2')
            else:
                link = 'https://app.nullphish.com/fy?id='+newtoken+'&template='+(str(templatename))
                link = [link]
                customsendphish(smtpserver, inserttemplate, receiveremail, firstname, lastname, subject, link, mailservbusiness)
                flash('Email sent to: '+receiveremail, 'category2')

    return render_template('schedulephish.html', businessdata=businessdata, availtemplates=availtemplates, serverlist=serverlist)    
