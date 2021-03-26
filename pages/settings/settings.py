from flask import Blueprint, render_template, redirect, url_for

# settings blueprint definition
settings = Blueprint('settings', __name__, static_folder='static', static_url_path='/settings', template_folder='templates')


# Routes
@settings.route('/settings')
def redirect_settings():
    return render_template('settings.html')
