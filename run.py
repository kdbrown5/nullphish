import os
from os import path, walk
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response
from flask_sqlalchemy import SQLAlchemy    

extra_dirs = ['templates/', ]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

app = Flask(__name__, static_url_path='', static_folder="static", template_folder="templates")
app.secret_key = 'Slskdjf2iu3#1!'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy()
routes = Blueprint('routes', __name__)

def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

def validate(username, password):
    con = sqlite3.connect('static/User.db')
    completion = False
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[1]
            dbPass = row[2]
            if dbUser == username:
                completion = check_password(dbPass, password)
    return completion

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def logina():
    if session.get('logged_in'):
        return redirect("/main")
    else:
        error = None
        if request.method == 'POST':
            username = request.form.to_dict()['username']
            password = request.form.to_dict()['password']
            completion = validate(username, password)
            if completion == False:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['username'] = (username)
                session['logged_in'] = True
                return redirect(url_for('main'))
        session['orderstatus'] = False
        return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def beginr():
    if session.get('logged_in'):
        return redirect('/main')
    else:
        return registration()

@app.route('/logout', methods=['GET', 'POST'])
def beginlogout():
    return logoutuser()

@app.route('/main', methods=['GET', 'POST'])
def main():    
    return render_template('intro.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)