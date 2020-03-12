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
            con.row_factory = sqlite.Row
            cur.execute('select name from templates where business LIKE (?) OR "nullphish";', (session['business'],))
            templateresults = cur.fetchall()
        con.close()
        return templateresults

    Path("./templates/businesses/"+str(session['business'])).mkdir(parents=True, exist_ok=True)
#    def templatesubmit():
    if request.method == "POST":
        try:
            savehtml = request.form.get('editordata')
            savehtmlnam = str(request.form.get('templatename'))
            savehtmlname = savehtmlnam+'.html'
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
                    cur.execute('insert into templates (business, name) VALUES (?,?);', (session['business'], savehtmlnam))
                    con.commit
                con.close
                flash('Submitted!', 'category2')
                return render_template("addtemplate.html", searchtemplates=searchtemplates)
        except:
            pass
    else:
        pass

    searchtemplates = templatelookup()

    return render_template("addtemplate.html", searchtemplates=searchtemplates)