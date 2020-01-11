import os
from os import path, walk
from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response

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


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

@app.route('/')


def mainpage():

    return render_template('prototype.html')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)