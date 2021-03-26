from flask import Blueprint, render_template, redirect, url_for

# favorites blueprint definition
favorites = Blueprint('favorites', __name__, static_folder='static', static_url_path='/favorites', template_folder='templates')


# Routes
@favorites.route('/favorites')
def redirect_favorites():
    return render_template('discussion_page.html')
