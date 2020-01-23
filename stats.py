import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from lumberjack import log

stats = Blueprint('stats', __name__, url_prefix='/stats', template_folder='templates')
@stats.route("/stats", methods=['GET', 'POST'])

def stat():
    def businesslookup():
        con = sqlite3.connect('static/db1.db')
        business = str(session['business'])
        business = business.replace('[', '')
        business = business.replace(']', '')
        with con:
            cur = con.cursor()
            businessquery = []
            for row in cur.execute('select DISTINCT * from tests where business LIKE (?);', (business,)):
                businessquery.append(row[:])
        con.close()
        businessdata = businessquery

        return businessquery

    def userlookup():
        con = sqlite3.connect('static/db1.db')
        business = str(session['business'])
        business = business.replace('[', '')
        business = business.replace(']', '')
        with con:
            cur = con.cursor()
            firstname = []
            lastname = []
            for row in cur.execute('select DISTINCT firstname from tests where business LIKE (?);', (business,)):
                row = str(row).replace('(', '')
                row = str(row).replace(')', '')
                row = str(row).replace(',', '')
                row = str(row).replace("'", '')
                firstname.append(row[:])
            for row in cur.execute('select DISTINCT lastname from tests where business LIKE (?);', (business,)):
                row = str(row).replace('(', '')
                row = str(row).replace(')', '')
                row = str(row).replace(',', '')
                row = str(row).replace("'", '')
                lastname.append(row[:])            
        con.close()
        return firstname, lastname

    def modifyuser(searchfirst, searchlast):
        con = sqlite3.connect('static/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('select * from tests where firstname LIKE (?) and lastname LIKE (?);', (searchfirst, searchlast),)
            usertests = cur.fetchall()
        con.close()
        return usertests

    def deleterecord(record):
        con = sqlite3.connect('static/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('delete from tests where id = (?);', (record),)
        con.close()
        return render_template('stats.html', businessdata=businessdata, firstlast=firstlast)

    businessdata = businesslookup()
    firstname, lastname = userlookup()
    firstlast = list(map(list, zip(firstname, lastname)))

    if 'modifyuser' in request.form:
        firstlast1 = request.form['modifyuser']
        firstlast1 = firstlast1.split(',')
        searchfirst = firstlast1[0][2:-1]
        searchlast = firstlast1[1][2:-2]
        usertests = modifyuser(searchfirst, searchlast)
        return render_template('stats.html', businessdata=businessdata, usertests=usertests)

    if 'deleterecord' in request.form:
        record = (request.form['deleterecord'][1])
        deleterecord(record)
        return render_template('stats.html', businessdata=businessdata, firstlast=firstlast)


    if 'main' in request.form:
        return redirect("/main")

    if 'Log Out' in request.form:
        session['logged_in'] = False
        return redirect("/stats")


    return render_template('stats.html', businessdata=businessdata, firstlast=firstlast)
