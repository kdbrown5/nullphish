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
from pysqlcipher3 import dbapi2 as sqlite


db = SQLAlchemy()

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='templates')
@profile.route("/profile", subdomain='app', methods=['GET', 'POST'])

def myprofile():
    def checkpassword():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select password from users where username = (?);', (session['username'],))
            passwordstatus = cur.fetchone()
            return passwordstatus

    passwordstatus = checkpassword()

    if request.method == "POST":
        if 'password' in request.form:
            if len(str(request.form['password'])) > 8:
                if repeat != password:
                    flash('Your passwords do not match.  Please try again.', 'category2')
                    return render_template("userprofile.html")
                else:
                    password = argon2.using(rounds=4).hash(request.form.get('password'))
                    repeat = password = argon2.using(rounds=4).hash(request.form.get('repeat'))
                    con = sqlite.connect('db/db1.db')
                    with con:
                        cur = con.cursor()
                        cur.execute('PRAGMA key = '+dbkey+';')
                        cur.execute("UPDATE users set password = (?) WHERE username = (?);", (password, session['username'],))
                        con.commit()
                        gc.collect()
                        flash('Password Changed!', 'category2')       
                        return render_template("userprofile.html", username=session['username'], business=session['business'], department=session['department'], role=session['role'], fname=session['fname'], lname=session['lname'])
            else:
                flash('Password must be 8 characters or more.', 'category2')
                return render_template("userprofile.html", username=session['username'], business=session['business'], department=session['department'], role=session['role'], fname=session['fname'], lname=session['lname'])

    if passwordstatus == None:
        flash('Please create a password for this account', 'category2')
        flash('(password requirements: more than 10 characters)', 'category1')
        return render_template('userprofile.html', username=session['username'], business=session['business'], department=session['department'], role=session['role'], fname=session['fname'], lname=session['lname'])

    return render_template("userprofile.html", username=session['username'], business=session['business'], department=session['department'], role=session['role'], fname=session['fname'], lname=session['lname'])