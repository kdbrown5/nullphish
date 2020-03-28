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
            userquery = []
            for row in cur.execute('select username from users where business = (?) and role = "user";', (session['business'],)):
                userquery.append(row[:][0])
        con.close()
        return userquery

    def adminuserlookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            con.row_factory = sqlite.Row
            adminquery = []
            for row in cur.execute('select username from users where role = "admin" or business = (?);', (session['business'],)):
                adminquery.append(row[:][0])
            rolequery = []
            for row in cur.execute('select role from users where role = "admin" or business = (?);', (session['business'],)):
                rolequery.append(row[0])
        con.close()
        return adminquery, rolequery

    def userlookup(emulateuserrequest):
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select firstname from users where username = (?);', (emulateuserrequest))
            emulatefname = cur.fetchone()
            emulatefname = emulatefname[0]
            cur.execute('select lastname from users where username = (?);', (emulateuserrequest))
            emulatelname = cur.fetchone()
            emulatelname = emulatelname[0]
            cur.execute('select department from users where username = (?);', (emulateuserrequest))
            emulatedept = cur.fetchone()
            emulatedept = emulatedept[0]
        con.close()
        return emulatefname, emulatelname, emulatedept

    if session['role'] == 'admin':
        userlist = reguserlookup()
    if session['role'] == 'superadmin':
        userlist, rolequery = adminuserlookup()
    
    if request.method == 'POST':
        emulateuserrequest = request.form.get('emulaterequest')
        emulateuserrequest = [emulateuserrequest]
        session['fname'], session['lname'], session['department'] = userlookup(emulateuserrequest)
        emulateuserrequest = emulateuserrequest[0]
        session['username'] = emulateuserrequest
        session['role'] = 'user'
        session['validated'] = 1
        return redirect ('/profile')

    return render_template('emulatelogin.html', userlist=userlist, rolequery=rolequery)