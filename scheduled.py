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
    def getlastsent():
        con = sqlite.connect('db/db1.db')
        cur = con.cursor()
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from (select id, department, username, template, mailname, bitly, admin, sentdate, scheduler from phishsched where business = (?) and sentdate != "none" ORDER BY ID DESC LIMIT 10) order by id asc;', (session['business'],))
        lastsent = cur.fetchall()
        try:
            con.close()
        except:
            pass
        return lastsent


    def getschedule():
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select id, username, template, mailname, date, bitly, admin, scheduler from phishsched where business = (?) and sentdate = "none";', (session['business'],),)
        result = cur.fetchall()
        try:
            con.close()
        except:
            pass
        return result

    def deleteDBrow(rowid, business, email, date):
        con = sqlite.connect('db/db1.db')
        cur = con.cursor()
        with con:
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('delete from phishsched where id = (?) and business = (?);', (rowid, session['business'],))
        con.close()
        dellist.append('Scheduled send for: '+email+' at'+date+' - deleted!')

    busdict = getschedule()
    lastsent = getlastsent()
    print(lastsent)
    print(type(lastsent))
    try:
        for i in lastsent:
            print(type(i))
            print(i)
    except:
        print('cant print i in lastsent')
    
    if request.method == 'POST':
        if 'email' in request.form:
            getemail = request.form.to_dict(flat=False)['email']
            getdate = request.form.to_dict(flat=False)['date']
            gettemplates = request.form.to_dict(flat=False)['template']
            getselect = request.form.to_dict(flat=False)['select']
            getserver = request.form.to_dict(flat=False)['mailname']
            getbitly = request.form.to_dict(flat=False)['bitly']
            getid = request.form.to_dict(flat=False)['id']
            dellist = []
            errlist = []
            errcount = 0
            for (g0, g1, g2, g3, g4, g5, g6) in zip(getselect, getid, getemail, gettemplates, getserver, getbitly, getdate):
                if g0 == "0":
                    pass
                else:
                    deleteDBrow(g1, session['business'], g2, g6)
                    for x in dellist:
                        flash(x, 'category2')
        else:
            flash('No records to delete', 'category2')

    return render_template('scheduled.html', busdict=busdict, lastsent=lastsent)    
