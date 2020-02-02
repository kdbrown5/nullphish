import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendphish(inserttemplate, receiveremail, firstname, lastname, subject):
    sender_email = "donotreply@nullphish.com"
    receiver_email = receiveremail
    password = "rtatstfu18as#R654"

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