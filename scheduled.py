import sqlalchemy
import flask
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from lumberjack import log
from maily import sendphish, customsendphish
from tokenizer import generate_confirmation_token, confirm_token
from pysqlcipher3 import dbapi2 as sqlite
from bitly import linkshorten
from datetime import datetime

scheduled = Blueprint('scheduled', __name__, url_prefix='/scheduled', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

@scheduled.route('/scheduled', methods=['GET', 'POST'])
def viewschedule():
    def getschedule():
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select id, username, template, mailname, date, bitly, subject, scheduler from phishsched where business = (?) and sentdate = "none";', (session['business'],),)
        result = cur.fetchall()
        try:
            con.close()
        except:
            pass
        return result

    busdict = getschedule()
    for i in busdict:
        for x in i:
            print(x)
    
    if request.method == 'POST':
        getemail = request.form.to_dict(flat=False)['email']
        getdate = request.form.to_dict(flat=False)['date']
        gettemplates = request.form.to_dict(flat=False)['template']
        getselect = request.form.to_dict(flat=False)['select']
        getserver = request.form.to_dict(flat=False)['mailname']
        getbitly = request.form.to_dict(flat=False)['bitly']
        getid = request.form.to_dict(flat=False)['id']
        sentlist = []
        errlist = []
        errcount = 0
        for (g0, g1, g2, g3, g4, g5, g6) in zip(getselect, getid, getemail, gettemplates, getserver, getbitly, getdate):
            if g0 == "0":
                pass
            else:
                print(g0, g1, g2, g3, g4, g5, g6)

    return render_template('scheduled.html', busdict=busdict)    
