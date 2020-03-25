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
from tokenizer import generate_confirmation_token, confirm_token
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db = SQLAlchemy()

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

adduser = Blueprint('adduser', __name__, url_prefix='/adduser', template_folder='templates')
@adduser.route("/adduser", subdomain='app', methods=['GET', 'POST'])
def addnewuser():
    def checkifexist(username):
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            con.row_factory = sqlite.Row
            print('query')
            print(cur.execute('select EXISTS ( select placeholder from users where username = (?) and business = (?));', (username, session['business'],)))
            cur.execute('select EXISTS ( select placeholder from users where username = (?) and business = (?));', (username, session['business'],))
            if cur.fetchone()[0] == 1:
                doesitexist = 0
            else:
                doesitexist = 1
            print('doesitexist')
            print(doesitexist)
        con.close()
        return doesitexist

    def reguserlookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            con.row_factory = sqlite.Row
            reguserquery = []
            for row in cur.execute('select username, firstname, lastname, department, role from users where business = (?);', (session['business'],)):
                reguserquery.append(row[:][0])
        con.close()
        return reguserquery

    def regsend(emailrecip, link, firstname):
        sender_email = "donotreply@nullphish.com"
        receiver_email = emailrecip
        password = "rtatstfu18as#R654"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome! Please complete registration"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        """

        changetemplate = open("templates/emailreg.html", "rt")###  read template and replace name 
        html = changetemplate.read()
        html = html.replace('username', firstname)
        html = html.replace('replacelink', link)
        changetemplate.close()

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first

        message.attach(part1)
        message.attach(part2)
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("webmail.nullphish.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    def registerreguser(rfname, rlname, rdpt, emailaddr, rrole):
        if len(str(rfname)) > 0:
            if len(str(rlname)) > 0:
                if len(str(emailaddr)) > 0:
                    if str(rrole) != str('Select Role'):
                        con = sqlite.connect('db/db1.db')
                        with con:
                            cur = con.cursor()
                            cur.execute('PRAGMA key = '+dbkey+';')
                            cur.execute('insert into users (username, firstname, lastname, role, department, validated, business) VALUES (?,?,?,?,?,0,?);', (emailaddr, rfname, rlname, rrole, rdpt, session['business'],))
                            con.commit
                        con.close
                        emailrecip = emailaddr
                        email = emailaddr
                        newtoken = generate_confirmation_token(email)
                        link = 'https://app.nullphish.com/register?token='+newtoken
                        firstname = rfname
                        regsend(emailrecip, link, firstname)
                        flash('Invitation Email sent to: '+emailrecip+'!', 'category2')
                        return render_template('adduser.html', lookup=lookup, username=session['username'])
                    else:
                        flash('Please select role', 'category2')
                        return render_template('adduser.html', lookup=lookup, username=session['username'])
                else:
                    flash('Please enter email address', 'category2')
                    return render_template('adduser.html', lookup=lookup, username=session['username'])
            else:
                flash('Please enter last name', 'category2')
                return render_template('adduser.html', lookup=lookup, username=session['username'])
        else:
            flash('Please enter first name', 'category2')
            return render_template('adduser.html', lookup=lookup, username=session['username'])

    lookup =  reguserlookup()

    if request.method == "POST":
        if 'emailaddr' in request.form:
            rfname = request.form['firstname']
            rlname = request.form['lastname']
            rdpt = request.form['department']
            emailaddr = request.form['emailaddr']
            rrole = request.form['addrole']
            doesitexist = checkifexist(emailaddr)
            if doesitexist == 0:
                flash('this user already exists', 'category2')
            else:
                if rrole == 'Admin':
                    rrole = 'admin'
                    registerreguser(rfname, rlname, rdpt, emailaddr, rrole)
                if rrole == 'User':
                    rrole = 'user'
                    registerreguser(rfname, rlname, rdpt, emailaddr, rrole)
                else:
                    flash('this is not a defined role', 'category2')
                    return render_template("adduser.html", lookup=lookup, username=session['username'])
            
        if 'password' in request.form:
            if len(str(request.form['password'])) > 8:
                if request.form['password'] != request.form['repeat']:
                    flash('Your passwords do not match.  Please try again.', 'category2')
                    return render_template("adduser.html")
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
                        return render_template("adduser.html", lookup=lookup, username=session['username'])
            else:
                flash('Password must be 8 characters or more.', 'category2')
                return render_template("adduser.html", lookup=lookup, username=session['username'])

    return render_template("adduser.html", lookup=lookup, username=session['username'])