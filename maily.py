import smtplib, ssl
import sqlalchemy
from pysqlcipher3 import dbapi2 as sqlite
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import urllib3
from urllib.request import urlopen
import base64

loadkey=open('../topseekrit', 'r')
dbkey=loadkey.read()
loadkey.close()

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

def bdecode(passw):
    notuple = convertTuple(str(passw))
    passw=notuple[2:-1]
    passw = bytes(passw, 'utf-8')
    if len(passw) % 4:
        # not a multiple of 4, add padding:
        passw += '=' * (4 - len(passw) % 4) 
    decoded = base64.b64decode(passw)
    makestr = decoded.decode('utf-8')
    return makestr

def sendphish(inserttemplate, receiveremail, firstname, lastname, subject, link):
    #sender_email = "donotreply@nullphish.com"
    sender_email = "donotreply@couponcheetah.com"
    receiver_email = receiveremail
    password = 'kirkland' # cheetah

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    """
    changetemplate = open(inserttemplate, "rt")###  read template and replace name 
    html = changetemplate.read()
    html = html.replace('firstname', firstname)
    html = html.replace('lastname', lastname)
    html = html.replace('receiveremail', receiveremail)
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
    #context = ssl.create_default_context()
    with smtplib.SMTP_SSL("webmail.nullphish.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def customsendphish(smtpserver, inserttemplate, receiveremail, firstname, lastname, subject, link, business):
    con = sqlite.connect('db/db1.db')
    print('sending ->', smtpserver, inserttemplate, receiveremail, firstname, lastname, subject, link, business)
    with con:
        cur = con.cursor()
        cur.execute('PRAGMA key = '+dbkey+';')
        mailsettings = []
        for row in cur.execute('select mailhost, mailuser, mailpass, mailtype, mailport from mailconfig where name = (?) and share = 1 or name = (?) and business = (?);', (smtpserver, smtpserver, business,)):
            mailsettings.append(row[:])
    con.close()
    sender_email = mailsettings[0][1]
    receiver_email = receiveremail
    codedpass = mailsettings[0][2]
    password = bdecode(codedpass)
    smtpserver = mailsettings[0][0]
    mailport = mailsettings[0][4]

    timestamp = (datetime.now())
    timestamp = timestamp.strftime("%m/%d/%Y %I:%M:%S %p")
    timestamp = timestamp.replace(' ', '-')

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    """
    changetemplate = open(inserttemplate, "rt")###  read template and replace name 
    html = changetemplate.read()
    html = html.replace('firstname', firstname)
    html = html.replace('lastname', lastname)
    html = html.replace('receiveremail', receiveremail)
    html = html.replace('datestamp', timestamp)
    html = html.replace('replacelink', str(link[0]))
    changetemplate.close()

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl._create_unverified_context()
    if mailport == 465 or mailport == "465":
        with smtplib.SMTP_SSL(smtpserver, mailport, context=ssl._create_unverified_context()) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    elif mailport == 587 or mailport == "587":
        with smtplib.SMTP(smtpserver, mailport) as server:
            server.starttls(context=ssl._create_unverified_context())
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    elif mailport == 25 or mailport == "25":
        with smtplib.SMTP(smtpserver, mailport) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )