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
                firstname.append(row[:])
            for row in cur.execute('select DISTINCT lastname from tests where business LIKE (?);', (business,)):
                lastname.append(row[:])            
        con.close()
        firstname = str(firstname)
        return firstname, lastname
    businessdata = businesslookup()
    firstname, lastname = userlookup()


    if 'main' in request.form:
        return redirect("/main")

    if 'Log Out' in request.form:
        session['logged_in'] = False
        return redirect("/stats")


    return render_template('stats.html', businessdata=businessdata)
