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
            print(email)
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
            xtemplate = ztemplate
            ztemplate = '/home/nullphish/prod/templates/businesses/'+zbusiness+'/'+ztemplate+'.html'
            zsubject = email[8]
            #zscheduler = email[10]
            #print('zscheduler')
            #print(zscheduler)
            #zadmin = email[11]
            #zdept = email[12]
            #print('zadmin')
            #print(zadmin)
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
                zlink = 'https://app.nullphish.com/fy?id='+ztoken+'&template='+(str(xtemplate))
                zlink = linkshorten(zlink)
                zlink = [zlink]
                zlink = zlink[0]
                customsendphish(zsender, ztemplate, zemail, zfirstname, zlastname, zsubject, zlink, zbusiness)
                cur.execute('update phishsched set sentdate = (datetime("now", "localtime")) where id = (?);', (zid,))
                cur.execute('update phishsched set token = (?) where id = (?);', (ztoken, zid,))
                #zemail, xtemplate, zsender, zdate, zbitly, zbusiness, zsubject, timestamp, zadmin, 
                #cur.execute('insert into emailpending (username, template, mailname, datesched, bitly, business, subject, sentdate, admin, department, idsched, token, phished) values (?,?,?,?,?,?,?,?,?,?,?,?,?);', ()
            else:
                zlink = 'https://app.nullphish.com/fy?id='+ztoken+'&template='+(str(xtemplate))
                zlink = [zlink]
                customsendphish(zsender, ztemplate, zemail, zfirstname, zlastname, zsubject, zlink, zbusiness)
                cur.execute('update phishsched set sentdate = (datetime("now", "localtime")) where id = (?);', (zid,))
                cur.execute('update phishsched set token = (?) where id = (?);', (ztoken, zid,))

@schedulephish.route('/schedulephish', methods=['GET', 'POST'])
def phishschedule():
    def businessdict():
        con = sqlite.connect('db/db1.db')
        con.row_factory = sqlite.Row
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        cur.execute('select * from users where business = ?;', (session['business'],))
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

    def lookupadmin():
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select username from users where notify = 1 and business = (?);', (business,))
            admins = cur.fetchone()
            admins = admins[0]
        con.close
        return admins

    def lookupemailsubject(templatename):
        business = str(session['business'])
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('select emailsubject from templates where business LIKE (?) and name LIKE (?);', (business, templatename,))
            emailsubject = cur.fetchone()
        con.close
        return emailsubject

    def scheduledb(username, template, mailname, date, bitly, business, subject, dept):
        print('sched')
        print(username, template, mailname, date, bitly, business, subject, dept)
        admins = lookupadmin()
        con = sqlite.connect('db/db1.db')
        with con:
            cur = con.cursor()
            cur.execute('PRAGMA key = '+dbkey+';')
            cur.execute('insert into phishsched ( type, scheduler, username, template, mailname, date, bitly, business, subject, admin, department) values ( "email", ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );', (session['username'], username, template, mailname, date, bitly, business, subject, admins, dept))
        con.close()

    availtemplates = lookuptemplates()
    serverlist = lookupmailserver()
    busdict = businessdict()
    
    if request.method == 'POST':
        if str(request.form.get('templateview')) != 'None':
            templateview = request.form.get('templateview')
            if templateview == 'prototype2':
                templateview = '/templates/prototype2.html'
                return render_template('schedulephish.html', busdict=busdict, availtemplates=availtemplates, templateview=templateview, serverlist=serverlist)
            else:
                templatecustom = 'businesses+^+'+session['business']+'+^+'+templateview+'.html'
                return render_template('schedulephish.html', busdict=busdict, availtemplates=availtemplates, templatecustom=templatecustom, serverlist=serverlist)
        else:
            getfirstname = request.form.to_dict(flat=False)['firstname']
            getlastname = request.form.to_dict(flat=False)['lastname']
            getemail = request.form.to_dict(flat=False)['email']
            getdate = request.form.to_dict(flat=False)['datetimepicker']
            gettemplates = request.form.to_dict(flat=False)['templates']
            getselect = request.form.to_dict(flat=False)['select']
            getserver = request.form.to_dict(flat=False)['smtpserver']
            getbitly = request.form.to_dict(flat=False)['bitly']
            getdept = request.form.to_dict(flat=False)['dept']
            sentlist = []
            errlist = []
            errcount = 0
            for (g1, g2, g3, g4, g5, g6, g7, g8, g9) in zip(getselect, getfirstname, getlastname, getemail, gettemplates, getserver, getbitly, getdate, getdept):
                if g1 == "0":
                    pass
                else:
                    if g6 == '':
                        #g4 = [g4]
                        errcount = errcount+1
                        errlist.append('Err: '+g4+' has no server assigned')
                        pass
                    if g8 == '':
                        #g4 = [g4]
                        errcount = errcount+1
                        errlist.append('Err: '+g4+' has no date')
                        pass
                    if g5 == '':
                        #g4 = [g4]
                        errcount = errcount+1
                        errlist.append('Err: '+g4+' has no template')
                        pass
                    if errcount != 0:
                        errlist = str(errlist)
                        errlist = errlist.replace("'", '')
                        errlist = errlist.replace("[", '')
                        errlist = errlist.replace("]", '')
                        flash(errlist, 'category2')
                        return render_template('schedulephish.html', busdict=busdict, availtemplates=availtemplates, serverlist=serverlist)    
                    g4a = [g4]
                    sentlist.append(g4a)
                    newtoken = generate_confirmation_token(g4)
                    subject = lookupemailsubject(g5)
                    subject = subject[0]
                    if g7 == "short":
                        #link = 'https://app.nullphish.com/fy?id='+newtoken+'&template='+(str(g5))
                        #link = linkshorten(link)
                        scheduledb(g4, g5, g6, g8, "1", session['business'], subject, g9 )
                        #customsendphish(g6, template, g4, g2, g3, subject, link, g6) # instant send
                    else:
                        #link = 'https://app.nullphish.com/fy?id='+newtoken+'&template='+(str(g5))
                        #link = [link]
                        scheduledb(g4, g5, g6, g8, "0", session['business'], subject, g9 )
                        #customsendphish(g6, template, g4, g2, g3, subject, link, g6) # instant send
            sentlist = (''.join(str(sentlist)))
            sentlist = sentlist.replace("],", ',')
            sentlist = sentlist.replace ("'", '')
            sentlist = sentlist.replace(']', '')
            sentlist = sentlist.replace('[', '')
            flash('Emails scheduled for: '+sentlist, 'category2')
        
    return render_template('schedulephish.html', busdict=busdict, availtemplates=availtemplates, serverlist=serverlist)    