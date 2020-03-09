import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from lumberjack import log
from maily import sendphish
from tokenizer import generate_confirmation_token, confirm_token
from pysqlcipher3 import dbapi2 as sqlite

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
        con = sqlite.connect('db/db1.db')
        business = str(session['business'])
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            serverlist = []
            for row in cur.execute('select mailuser from mailconfig where business LIKE (?) OR "nullphish";', (business,)):
                serverlist.append(row[:])
        con.close()
        return serverlist

    def lookuptemplates():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            templatelist = []
            for row in cur.execute('select name from templates where business LIKE (?) OR "nullphish";', (business,)):
                templatelist.append(row[:][0])
            con.close
        return templatelist

    availtemplates = lookuptemplates()
    print(availtemplates)
    #availtemplates = ['amazon', 'prototype2', 'starbucks']

    businessdata = businesslookup()
    serverlist = lookupmailserver()

    if request.method == 'POST':
        if str(request.form.get('templateview')) != 'None':
            templateview = request.form.get('templateview')
            return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, templateview=templateview)
        if str(request.form.get('templateview')) == 'None':
            templatechoice = request.form.get('templates')
            templatechoice = 'templates/'+str(templatechoice)+'.html'
        if '@' not in request.form.get('email'):
            flash('This is not a valid email address', 'category2')
        else:
            inserttemplate = templatechoice
            receiveremail = request.form.get('email')
            newtoken = generate_confirmation_token(receiveremail)
            link = 'https://app.nullphish.com/fy?id='+newtoken
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            subject = firstname+', this FREE drink is on us!'
            sendphish(inserttemplate, receiveremail, firstname, lastname, subject, link)


    if 'exitmodify' in request.form:
        return redirect('/stats')

    return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, serverlist=serverlist)    
