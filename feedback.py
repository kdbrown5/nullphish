import requests
import sqlalchemy
from sqlalchemy import event, PrimaryKeyConstraint
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from pysqlcipher3 import dbapi2 as sqlite
from bs4 import BeautifulSoup as bs4

db = SQLAlchemy()

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

feedback = Blueprint('feedback', __name__, url_prefix='/feedback', template_folder='templates')
@feedback.route("/feedback", subdomain='app', methods=['GET', 'POST'])

def getfeedback():
    def emailfeedback(feedbackhtml):
        sender_email = "donotreply@nullphish.com"
        receiver_email = 'kdbrown5@gmail.com'
        password = "rtatstfu18as#R654"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "User Feedback - NullPhish"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        """

        feedbackhtml = session['username']+'<br><br>'+feedbackhmtl
        html = feedbackhtml

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

    if request.method == "POST":
        if request.form.get('editordata') != None:
            #try:
            savefeedback = request.form.get('editordata')
            emailfeedback(savefeedback)
            flash('Submitted! Thank you for the feedback', 'category2')
            return render_template("feedback.html")
            #except:
                pass


    return render_template("feedback.html")