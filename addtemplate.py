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
from pathlib import Path
import os.path
import re
from bs4 import BeautifulSoup as bs4

db = SQLAlchemy()

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

addtemplate = Blueprint('addtemplate', __name__, url_prefix='/addtemplate', template_folder='templates')
@addtemplate.route("/adduser", subdomain='app', methods=['GET', 'POST'])

def addnewtemplate():
    def templatelookup():
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            templateresults = []
            for row in cur.execute('select name from templates where business LIKE (?);', (session['business'],)):
                templateresults.append(row[:][0])
        con.close()
        return templateresults

    Path("./templates/businesses/"+str(session['business'])).mkdir(parents=True, exist_ok=True)
#    def templatesubmit():
    if request.method == "POST":
        if request.form.get('editordata') != None:
            try:
                savehtml = request.form.get('editordata')
                soup = bs(savehtml)
                for a in soup.findAll('a'):
                    a['href'] = "replacelink"
                print(soup)
                savehtml = soup
                savehtmlnam = str(request.form.get('templatename'))
                savehtmlname = savehtmlnam+'.html'
                templatesubject = request.form.get('templatesubject')
                if os.path.isfile('./templates/businesses/'+session['business']+'/'+savehtmlname):
                    flash('A template with this name already exists', 'category2')
                    return render_template("addtemplate.html", searchtemplates=searchtemplates)
                else:
                    with open('./templates/businesses/'+session['business']+'/'+savehtmlname, 'w') as f:
                        f.write(savehtml)
                    con = sqlite.connect('db/db1.db')
                    with con:
                        cur = con.cursor()
                        cur.execute('PRAGMA key = '+dbkey+';')
                        cur.execute('insert into templates (business, name, emailsubject) VALUES (?,?,?);', (session['business'], savehtmlnam, templatesubject))
                        con.commit
                    con.close
                    flash('Submitted!', 'category2')
                    return render_template("addtemplate.html", searchtemplates=searchtemplates)
            except:
                pass
        if request.form.get('selecttemplate') != 'Templates':
            if request.form.get('selecttemplate') != None:
                selecttemplate = request.form.get('selecttemplate')
                if selecttemplate == 'prototype2':
                    flash('No deleting default templates', 'category2')
                elif selecttemplate == 'amazon':
                    flash('No deleting default templates', 'category2')
                elif selecttemplate == 'starbucks':
                    flash('No deleting default templates', 'category2')
                else:
                    con = sqlite.connect('db/db1.db')
                    with con:
                        cur = con.cursor()
                        cur.execute('PRAGMA key = '+dbkey+';')
                        cur.execute('delete from templates where business LIKE (?) and name LIKE (?);', (session['business'], selecttemplate,))
                    con.close()
                    os.remove('./templates/businesses/'+session['business']+'/'+selecttemplate+'.html')
                    flash('Deleted!', 'category2')

    else:
        pass

    searchtemplates = templatelookup()

    return render_template("addtemplate.html", searchtemplates=searchtemplates)