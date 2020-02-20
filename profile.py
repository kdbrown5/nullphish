import requests
import sqlalchemy
import hashlib
from sqlalchemy import event, PrimaryKeyConstraint
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
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

profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='templates')
@profile.route("/profile", subdomain='app', methods=['GET', 'POST'])

def myprofile():
    def reguserlookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            con.row_factory = sqlite.Row
            cur.execute('select firstname, lastname, department, role from users where business = (?);', (session['business'],))
            reguserquery = cur.fetchall()
        con.close()
        return reguserquery

    def rolelookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            con.row_factory = sqlite.Row
            cur.execute('select role from users where username = (?);', (session['username'],))
            currentrole = cur.fetchall()
            currentrole = str(currentrole[0])
            currentrole = currentrole[2:-3]
        con.close()
        return currentrole

    def checkpassword():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select password from users where username = (?);', (session['username'],))
            passwordstatus = cur.fetchone()
            return passwordstatus

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
                            cur.execute('insert into users (username, firstname, lastname, role, department, validated) VALUES (?,?,?,?,?,0);', (emailaddr, rfname, rlname, rrole, rdpt))
                            con.commit
                        con.close
                        emailrecip = emailaddr
                        email = emailaddr
                        newtoken = generate_confirmation_token(email)
                        link = 'https://app.nullphish.com/register?token='+newtoken
                        firstname = rfname
                        regsend(emailrecip, link, firstname)
                        flash('Invitation Email sent to: '+emailrecip+'!', 'category2')
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

    lookup =  reguserlookup()
    passwordstatus = checkpassword()
    currentrole = rolelookup()

    if request.method == "POST":
        if 'emailaddr' in request.form:
            rfname = request.form['firstname']
            rlname = request.form['lastname']
            rdpt = request.form['department']
            emailaddr = request.form['emailaddr']
            rrole = request.form['addrole']
            registerreguser(rfname, rlname, rdpt, emailaddr, rrole)
            
        if 'password' in request.form:
            print(str(request.form['password']))
            if len(str(request.form['password'])) > 8:
                #password = sha256_crypt.encrypt((str(request.form.get('password'))))
                password = hashlib.md5(str(request.form.get('password')).encode()).hexdigest()
                repeat = hashlib.md5(str(request.form.get('repeat')).encode()).hexdigest()
                if repeat != password:
                    flash('Your passwords do not match.  Please try again.', 'category2')
                    if currentrole == "User":
                        return render_template('userprofile.html')
                    else:
                        return render_template("profile.html")
                con = sqlite.connect('db/db1.db')
                with con:
                    cur = con.cursor()
                    cur.execute('PRAGMA key = '+dbkey+';')
                    cur.execute("UPDATE users set password = (?) WHERE username = (?);", (password, session['username'],))
                    con.commit()
                    gc.collect()
                    flash('Password Changed!', 'category2')       
                    if currentrole == "User":
                        return render_template('userprofile.html')
                    else:
                        return render_template("profile.html", lookup=lookup)
            else:

                flash('Password must be 8 characters or more.', 'category2')
                if currentrole == "User":
                    return render_template('userprofile.html')
                else:
                    return render_template("profile.html", lookup=lookup)

    if passwordstatus == None:
        flash('Please create a password for this account', 'category2')
        flash('(password requirements: more than 10 characters)', 'category1')
        return render_template('userprofile.html', lookup=lookup)

    if currentrole == "User":
        return render_template('userprofile.html')


    return render_template("profile.html", lookup=lookup)