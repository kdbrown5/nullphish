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

schedulephish = Blueprint('schedulephish', __name__, url_prefix='/schedulephish', template_folder='templates')

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

def checkschedule():
    con = sqlite.connect('db/db1.db')
    with con:
        emailsched = []
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        for row in cur.execute('select * from phishsched where type = "email" and date between "2020-04-01" and DATETIME("now", "localtime", "+5 minutes") and sentdate = "none";'):
            emailsched.append(row[:])
        for email in emailsched:
            timestamp = (datetime.now())
            timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
            timestamp = timestamp.replace(' ', '-')
            zid = email[0]
            #ztype = email[1]
            zemail = email[2]
            zemail = [zemail]
            zemail = zemail[0]
            ztemplate = email[3]
            zsender = email[4]
            zsender = convertTuple(zsender)
            #zdate = email[5]
            zbitly = email[6]
            zbusiness = email[7]
            zbusiness = [zbusiness]
            zbusiness = zbusiness[0]
            ztemplate = '/home/nullphish/prod/templates/businesses/'+zbusiness+'/'+ztemplate+'.html'
            zsubject = email[8]
            cur.execute('select firstname from users where username = (?);', (zemail,))
            zfirstname = cur.fetchall()
            zfirstname = str(zfirstname[0])
            zfirstname = zfirstname.replace("('", '')
            zfirstname = zfirstname.replace("',)", '')
            cur.execute('select lastname from users where username = (?);', (zemail,))
            zlastname = cur.fetchall()
            zlastname = str(zlastname[0])
            zlastname = zlastname.replace("('", '')
            zlastname = zlastname.replace("',)", '')
            ztoken = generate_confirmation_token(zemail)
            timestamp = [timestamp]
            timestamp = convertTuple(timestamp[0])
            if zbitly == 1:
                zlink = 'https://app.nullphish.com/fy?id='+ztoken+'&template='+(str(ztemplate))
                zlink = linkshorten(zlink)
                zlink = [zlink]
                zlink = zlink[0]
                customsendphish(zsender, ztemplate, zemail, zfirstname, zlastname, zsubject, zlink, zbusiness)
                cur.execute('update phishsched set sentdate = (datetime("now", "localtime")) where id = (?);', (zid,))
            else:
                zlink = 'https://app.nullphish.com/fy?id='+ztoken+'&template='+(str(ztemplate))
                zlink = [zlink]
                customsendphish(zsender, ztemplate, zemail, zfirstname, zlastname, zsubject, zlink, zbusiness)
                cur.execute('update phishsched set sentdate = (datetime("now", "localtime")) where id = (?);', (zid,))     

@schedulephish.route('/schedulephish', methods=['GET', 'POST'])
def phishschedule():
    def businesslookup():
        con = sqlite.connect('db/db1.db')
        business = str(session['business'])
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            businessquery = []
            for row in cur.execute('select * from users where business LIKE (?);', (business,)):
                businessquery.append(row[:])
        con.close()
        businessdata = businessquery
        return businessdata

    def businessdict():
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from users')
        result = cur.fetchall()
        try:
            con.close()
        except:
            pass
        return result

    def lookupmailserver():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            serverlist = []
            for row in cur.execute('select name from mailconfig where business = (?) OR share = 1;', (business,)):
                serverlist.append(row[:][0])
        con.close()
        return serverlist

    def lookuptemplates():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            templatelist = []
            for row in cur.execute('select name from templates where business = (?) or shared = 1;', (business,)):
                templatelist.append(row[:][0])
            con.close
        return templatelist

    def convertTuple(tup): 
        str =  ''.join(tup) 
        return str

    def lookupemailsubject(templatename):
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select emailsubject from templates where business LIKE (?) and name LIKE (?);', (business, templatename,))
            print(cur.fetchall())
            emailsubject = cur.fetchone()
        con.close
        #emailsubject = convertTuple(emailsubject)
        return emailsubject
    
    def generatearray():
        arrayid = []
        xid = 0
        for item in businessdata:
            xid = xid+1
            arrayid.append(xid)
        return arrayid

    availtemplates = lookuptemplates()
    businessdata = businesslookup()
    serverlist = lookupmailserver()
    arrayid = generatearray()
    busdict = businessdict()
    
    if request.method == 'POST':
        print(request.form)
        getfirstname = request.form.to_dict(flat=False)['firstname']
        getlastname = request.form.to_dict(flat=False)['lastname']
        getemail = request.form.to_dict(flat=False)['email']
        getdate = request.form.to_dict(flat=False)['datetimepicker']
        gettemplates = request.form.to_dict(flat=False)['templates']
        getselect = request.form.to_dict(flat=False)['select']
        getserver = request.form.to_dict(flat=False)['smtpserver']
        getbitly = request.form.to_dict(flat=False)['bitly']
        print('---------')
        for (g1, g2, g3, g4, g5, g6, g7, g8) in zip(getselect, getfirstname, getlastname, getemail, gettemplates, getserver, getbitly, getdate):
            if g1 == "0":
                pass
            else:
                print(g2, g3, g4, g5, g6, g7, g8)
                newtoken = generate_confirmation_token(g4)
                subject = lookupemailsubject(g5)
                print('sub')
                print(subject)
                print('end sub')    
                if g7 == "short":
                    link = 'https://app.nullphish.com/fy?id='+newtoken+'&template='+(str(templatename))
                    link = linkshorten(link)
                    customsendphish(g6, g5, g4, g2, g3, subject, link, g6)
                    flash('Email sent to: '+g6, 'category2')
                else:
                    link = 'https://app.nullphish.com/fy?id='+newtoken+'&template='+(str(templatename))
                    link = [link]
                    customsendphish(g6, g5, g4, g2, g3, subject, link, g6)
                    flash('Email sent to: '+g6, 'category2')

    return render_template('schedulephish.html', busdict=busdict, arrayid=arrayid, businessdata=businessdata, availtemplates=availtemplates, serverlist=serverlist)    
