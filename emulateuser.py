import requests
import sqlalchemy
import hashlib
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from pysqlcipher3 import dbapi2 as sqlite

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

emulateuser = Blueprint('emulateuser', __name__, url_prefix='/emulateuser', template_folder='templates')
@emulateuser.route("/emulateuser", subdomain='app', methods=['GET', 'POST'])

def emulatelogin():
    def reguserlookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            con.row_factory = sqlite.Row
            cur.execute('select username from users where business = (?);', (session['business'],))
            reguserquery = cur.fetchall()[0]
        con.close()
        return reguserquery

    userlist = reguserlookup()
    print(session['business'])
    
    if request.method == 'POST':
        emulateuserrequest = request.form.get('emulaterequest')
        print(emulateuserrequest)
        session['username'] = emulateuserrequest
        session['role'] = 'user'
        session['validated'] = 1
        return redirect ('/profile')

    return render_template('emulatelogin.html', userlist=userlist)