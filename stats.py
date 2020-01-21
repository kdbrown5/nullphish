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
        username = session['username']
        with con:
            cur = con.cursor()
            cur.execute('select * from tests where business LIKE (?);', (str(session['business']),))
            businessquery2 = str(cur.fetchone())
            businessquery = str(cur.fetchall())
            print(businessquery2)
            print(businessquery)
        con.close()
        return businessquery

    businessdata = businesslookup()
    print(businessdata)

    if 'main' in request.form:
        return redirect("/main")

    if 'Log Out' in request.form:
        session['logged_in'] = False
        return redirect("/stats")


    return render_template('stats.html', businessdata=businessdata)
