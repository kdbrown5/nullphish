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

gophishing = Blueprint('gophishing', __name__, url_prefix='/gophishing', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

@gophishing.route('/gophishing', methods=['GET', 'POST'])
def gophish():
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
    #availtemplates = ['amazon', 'prototype2', 'starbucks']

    businessdata = businesslookup()
    serverlist = lookupmailserver()

    if request.method == 'POST':
        if str(request.form.get('templateview')) != 'None':
            templateview = request.form.get('templateview')
            if templateview == 'prototype2':
                templateview = '/templates/prototype2.html'
                return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, templateview=templateview, serverlist=serverlist)
            else:
                templatecustom = 'businesses+^+'+session['business']+'+^+'+templateview+'.html'
                return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, templatecustom=templatecustom, serverlist=serverlist)
        if str(request.form.get('templateview')) == 'None':
            templatechoice = request.form.get('templates')
            templatename = templatechoice
            templatechoice = str(templatechoice)+'.html'
        if '@' not in request.form.get('email'):
            flash('This is not a valid email address', 'category2')
        if request.form.get('smtpserver') == 'Mail Server':
            flash('Please choose a mail server', 'category2')
            return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, serverlist=serverlist)
        if request.form.get('templates') == 'Templates':
            flash('Please choose a template', 'category2')
            return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, serverlist=serverlist)
        else:
            if templatechoice == 'amazon.html' or templatechoice == 'starbucks.html' or templatechoice == 'prototype2.html':
                inserttemplate = 'templates/'+templatechoice
            else:
                inserttemplate = '/home/nullphish/prod/templates/businesses/'+session['business']+'/'+templatechoice
            smtpserver = request.form.get('smtpserver')
            if smtpserver == 'couponcheetah.com':
                mailservbusiness = 'public'
            else:
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
                customsendphish(smtpserver, inserttemplate, receiveremail, firstname, lastname, subject, link, mailservbusiness)
                flash('Email sent to: '+receiveremail, 'category2')
            
    if 'exitmodify' in request.form:
        return redirect('/stats')

    return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, serverlist=serverlist)    
