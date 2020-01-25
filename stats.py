import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from lumberjack import log


stats = Blueprint('stats', __name__, url_prefix='/stats', template_folder='templates')

@stats.route('/stats/mod', methods=['GET', 'POST'])
def waitforrecdel1():
    def businesslookup():
        con = sqlite3.connect('static/db1.db')
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

    if 'exitmodify' in request.form:
        return redirect('/stats')

    return render_template('stats-modify.html', businessdata=businessdata)    


@stats.route('/stats/del', methods=['GET', 'POST'])
def waitforrecdel():
    def businesslookup():
        con = sqlite3.connect('static/db1.db')
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
        con = sqlite3.connect('static/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('select business from tests where id = (?);', (delrec,))
            businessverify = cur.fetchone()
            if str(businessverify[0]) == str(session['business'][1:-1]):
                cur.execute('update tests set notify = 0 where id = (?);', (delrec,))
            else:
                flash('Why are you trying to hack the gibson?', 'category2')

    businessdata = businesslookup()

    if request.method == 'GET':
        print(request.args.get('rec'[:]))
        if request.args.get('rec'[:]) == None:
            return render_template('stats-modify.html', businessdata=businessdata)
        else:
            delrec = request.args.get('rec')
            deleterecord(delrec)
            return redirect('/stats/mod')

    if 'exitmodify' in request.form:
        return redirect('/stats')

    return render_template('stats-modify.html', businessdata=businessdata)    

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
