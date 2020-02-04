import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from lumberjack import log

stats = Blueprint('stats', __name__, url_prefix='/stats', template_folder='templates')

@stats.route('/stats/mod', methods=['GET', 'POST']) ### url to keep modification / record deletion open
def waitforrecdel1():
    def businesslookup():
        con = sqlite3.connect('db/db1.db')
        business = str(session['business'])
        business = business.replace('[', '')
        business = business.replace(']', '')
        with con:
            cur = con.cursor()
            businessquery = []
            for row in cur.execute('select DISTINCT * from tests where business LIKE (?) and notify = 1;', (business,)):## populate tables with user data from same business
                businessquery.append(row[:])
        con.close()
        businessdata = businessquery
        return businessquery
        
    businessdata = businesslookup()# return userdata list to render on page

    if 'exitmodify' in request.form:
        return redirect('/stats')

    return render_template('stats-modify.html', businessdata=businessdata)    


@stats.route('/stats/del', methods=['GET', 'POST'])
def waitforrecdel():
    def businesslookup():
        con = sqlite3.connect('db/db1.db')
        business = str(session['business'])
        business = business.replace('[', '')
        business = business.replace(']', '')
        with con:
            cur = con.cursor()
            businessquery = []
            for row in cur.execute('select DISTINCT * from tests where business LIKE (?) and notify = 1;', (business,)):
                businessquery.append(row[:])
        con.close()
        businessdata = businessquery
        return businessquery

    def deleterecord(delrec):
        con = sqlite3.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('select business from tests where id = (?);', (delrec,))# grab business name from test deletion request
            businessverify = cur.fetchone()
            if str(businessverify[0]) == str(session['business'][1:-1]):# compare test business name to admin user business name
                cur.execute('update tests set notify = 0 where id = (?);', (delrec,))# delete record
            else:
                flash('Why are you trying to hack the gibson?', 'category2')# someone is haxing us

    businessdata = businesslookup()

    if request.method == 'GET':
        if request.args.get('rec'[:]) == None:# if no record deletion requested
            return render_template('stats-modify.html', businessdata=businessdata)
        else:
            delrec = request.args.get('rec')# record deletion requested - ie - nullphish.com/stats/del?rec=5 as example
            deleterecord(delrec)
            return redirect('/stats/mod')# return to table w/ modification enabled render

    if 'exitmodify' in request.form:
        return redirect('/stats')# return to locked tables

    return render_template('stats-modify.html', businessdata=businessdata)    

@stats.route("/stats", methods=['GET', 'POST'])

def stat():
    def businesslookup():
        con = sqlite3.connect('db/db1.db')
        business = str(session['business'])
        business = business.replace('[', '')
        business = business.replace(']', '')
        with con:
            cur = con.cursor()
            businessquery = []
            for row in cur.execute('select DISTINCT * from tests where business LIKE (?) and notify = 1;', (business,)):
                businessquery.append(row[:])
        con.close()
        businessdata = businessquery
        return businessquery

    businessdata = businesslookup()

    if 'modifyrecord' in request.form:
        return render_template('stats-modify.html', businessdata=businessdata)

    if 'main' in request.form:
        return redirect("/main")

    if 'Log Out' in request.form:
        session['logged_in'] = False
        return redirect("/stats")

    return render_template('stats.html', businessdata=businessdata)
