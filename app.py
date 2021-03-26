from flask import Flask


###### App setup
app = Flask(__name__)
app.config.from_pyfile('settings.py')

###### Pages
## Homepage
from pages.homepage.homepage import homepage
app.register_blueprint(homepage)


## Page error handlers
from pages.page_error_handlers.page_error_handlers import page_error_handlers
app.register_blueprint(page_error_handlers)

## Components
from components.main_menu.main_menu import main_menu
app.register_blueprint(main_menu)

from components.header.header import header
app.register_blueprint(header)

from components.footer.footer import footer
app.register_blueprint(footer)

## Pages
from pages.settings.settings import settings
app.register_blueprint(settings)

from pages.favorites.favorites import favorites
app.register_blueprint(favorites)

from pages.profile.profile import profile
app.register_blueprint(profile)

from pages.discussions.discussions import discussions
app.register_blueprint(discussions)

