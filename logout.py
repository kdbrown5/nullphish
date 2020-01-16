from flask import Flask, flash, session, render_template, render_template_string, request, jsonify, redirect, url_for, \
    Response, g, Markup, Blueprint, make_response

logout = Blueprint('logout', __name__, url_prefix='/logout', template_folder='templates')
@logout.route("/logout", methods=['GET', 'POST'])

def logoutuser():
    session['logged_in'] = False
    return redirect("/login")