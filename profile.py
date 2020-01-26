import requests
import sqlalchemy
import sqlite3
import sqlite3 as sql
import hashlib
from sqlalchemy import event, PrimaryKeyConstraint
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
import gc

db = SQLAlchemy()
profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='templates')
@profile.route("/profile", methods=['GET', 'POST'])

def myprofile():
    def studentlookup():
        username = session['username']
        con = sqlite3.connect('static/db1.db')
        with con:
            cur = con.cursor()
            con.row_factory = sql.Row
            cur.execute('select firstname, lastname, department, role from users where business = (?);', (session['business'],))
            studentquery = cur.fetchall()
        con.close()
        return studentquery

    def registerstudent(rfname, rlname, rdpt, emailaddr, rrole):
        if len(str(rfname)) > 0:
            if len(str(rlname)) > 0:
                if len(str(emailaddr)) > 0:
                    if str(rrole) != str('Select Role'):
                        con = sqlite3.connect('static/db1.db')
                        with con:
                            cur = con.cursor()
                            cur.execute('insert into users (username, firstname, lastname, role, department) VALUES (?,?,?,?,?);', (emailaddr, rfname, rlname, rrole, rdpt))
                            con.commit
                        con.close
                        flash('Member Added!', 'category2')
                        return redirect('/profile')
                    else:
                        flash('Please select role', 'category2')
                        return render_template('profile.html', lookup=lookup)
                else:
                    flash('Please enter email address', 'category2')
                    return render_template('profile.html', lookup=lookup)
            else:
                flash('Please enter last name', 'category2')
                return render_template('profile.html', lookup=lookup)
        else:
            flash('Please enter first name', 'category2')
            return render_template('profile.html', lookup=lookup)

    lookup =  studentlookup()

    if request.method == "POST":
        if 'emailaddr' in request.form:
            rfname = request.form['firstname']
            rlname = request.form['lastname']
            rdpt = request.form['department']
            emailaddr = request.form['emailaddr']
            rrole = request.form['addrole']
            registerstudent(rfname, rlname, rdpt, emailaddr, rrole)
            
        if 'password' in request.form:
            print(str(request.form['password']))
            if len(str(request.form['password'])) > 8:
                #password = sha256_crypt.encrypt((str(request.form.get('password'))))
                password = hashlib.md5(str(request.form.get('password')).encode()).hexdigest()
                repeat = hashlib.md5(str(request.form.get('repeat')).encode()).hexdigest()
                if repeat != password:
                    flash('Your passwords do not match.  Please try again.', 'category2')
                    return render_template("profile.html")
                con = sqlite3.connect('static/db1.db')
                with con:
                    cur = con.cursor()
                    cur.execute("UPDATE users set password = (?) WHERE username = (?);", (password, session['username'],))
                    con.commit()
                    gc.collect()
                    flash('Password Changed!', 'category2')            
                    return render_template("profile.html", lookup=lookup)   
            else:
                flash('Password must be 8 characters or more.', 'category2')
                return render_template("profile.html", lookup=lookup) 

    return render_template("profile.html", lookup=lookup)