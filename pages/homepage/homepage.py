from flask import Blueprint, render_template, redirect, url_for, session
from utilities.db.quries import DBQuery
# homepage blueprint definition
homepage = Blueprint('homepage', __name__, static_folder='static', static_url_path='/homepage', template_folder='templates')


# Routes
@homepage.route('/')
def index():
    session['logged_in'] = False
    session['email'] = 'guest@guest.guest'
    session['name'] = 'Guest'
    return redirect('homepage')


@homepage.route('/homepage')
def redirect_homepage():
    return render_template('homepage.html')


