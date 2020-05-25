import requests
import sqlalchemy
import hashlib
from sqlalchemy import event, PrimaryKeyConstraint
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt, argon2
import gc
from register import register, registration
from tokenizer import generate_confirmation_token, confirm_token
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pysqlcipher3 import dbapi2 as sqlite

db = SQLAlchemy()

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

adminprofile = Blueprint('adminprofile', __name__, url_prefix='/adminprofile', template_folder='templates')
@adminprofile.route("/adminprofile", subdomain='app', methods=['GET', 'POST'])

def loadadminprofile():
    def placeholder():
        print(';')

    def loadmessages(): 
        currentmessages = []
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            for row in cur.execute("select sender, message from messages where username = (?) and business = (?);", (session['username'], session['business'],)):
                currentmessages.append(row[0]+': '+row[1])
        print(currentmessages)
        return currentmessages

    try:
        currentmessages = loadmessages()
        flash(currentmessages, 'category1')
    except:
        print('no messages-syslog')
        pass

    if request.method == "POST":
        if 'password' in request.form:
            if len(str(request.form['password'])) > 8:
                if request.form['password'] != request.form['repeat']:
                    flash('Your passwords do not match.  Please try again.', 'category2')
                    return render_template("adminprofile.html")
                else:
                    password = argon2.using(rounds=4).hash(request.form.get('password'))
                    con = sqlite.connect('db/db1.db')
                    with con:
                        cur = con.cursor()
                        cur.execute('PRAGMA key = '+dbkey+';')
                        cur.execute("UPDATE users set password = (?) WHERE username = (?);", (password, session['username'],))
                        con.commit()
                        gc.collect()
                        flash('Password Changed!', 'category2')       
                        return render_template("adminprofile.html", username=session['username'], business=session['business'], department=session['department'], role=session['role'], firstname=session['fname'], lastname=session['lname'])
            else:
                flash('Password must be 8 characters or more.', 'category2')
                return render_template("adminprofile.html", username=session['username'], business=session['business'], department=session['department'], role=session['role'], firstname=session['fname'], lastname=session['lname'])

    return render_template("adminprofile.html", username=session['username'], business=session['business'], department=session['department'], role=session['role'], firstname=session['fname'], lastname=session['lname'])