import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from lumberjack import log
from maily import sendphish


gophishing = Blueprint('gophishing', __name__, url_prefix='/gophishing', template_folder='templates')

@gophishing.route('/gophishing', methods=['GET', 'POST'])
def gophish():
    def businesslookup():
        con = sqlite3.connect('static/db1.db')
        business = str(session['business'])
        with con:
            cur = con.cursor()
            businessquery = []
            for row in cur.execute('select DISTINCT * from users where business LIKE (?);', (business,)):
                businessquery.append(row[:])
        con.close()
        businessdata = businessquery
        return businessdata
    availtemplates = ['amazon', 'prototype2', 'starbucks']
    businessdata = businesslookup()

    if request.method == 'POST':
        if request.form.get('templateview') != 'Templates':
            templateview = request.form.get('templateview')
            return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates, templateview=templateview)
        templatechoice = request.form.get('templates')
        templatechoice = 'templates/'+templatechoice+'.html'
        if '@' not in request.form.get('email'):
            flash('This is not a valid email address', 'category2')
        else:
            inserttemplate = templatechoice
            receiveremail = request.form.get('email')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            subject = firstname+', you have received a new document'
            sendphish(inserttemplate, receiveremail, firstname, lastname, subject)


    if 'exitmodify' in request.form:
        return redirect('/stats')

    return render_template('gophishing.html', businessdata=businessdata, availtemplates=availtemplates)    