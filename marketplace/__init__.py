# Initialisation file.
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_wtf import CSRFProtect


# Database.
db=SQLAlchemy()

# Function for creating a web app to be run by the server.
def create_app():

    app=Flask(__name__)  # Name of the module/package that is calling this app.
    app.debug=True
    app.secret_key='utroutoru'
    # Set the app configuration data.
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///marketplace.sqlite'
    # Initialize database with Flask app.
    db.init_app(app)

    # Initialize Bootstrap with Flask app.
    bootstrap = Bootstrap(app)

    # Initialize the login manager.
    login_manager = LoginManager()

    # Set the name of the login function that lets users login.
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    # Error handling.
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('500.html'), 500


    # Importing modules here to avoid circular references.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import listings
    app.register_blueprint(listings.bp)

    from . import result
    app.register_blueprint(result.bp)

    from . import manage
    app.register_blueprint(manage.bp)

    # Login-related details.
    from .models import User

    

    class AnonymousUser(AnonymousUserMixin):
        id = -1

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_message_category = "info"

    csrf = CSRFProtect(app)

    # Image storage locations.
    UPLOAD_FOLDER = '/static/Images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    import os
    

    def create_app():
        app.config.from_mapping(
            # Flask-SQLAlchemy settings
            SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'],
        )

    return app
