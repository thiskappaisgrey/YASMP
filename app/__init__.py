#!/usr/bin/env python3
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy



def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    # db.init_app(app)

    with app.app_context():
        from . import db
        db.init_app(app)

        from . import auth
        app.register_blueprint(auth.bp)

        from . import blog
        app.register_blueprint(blog.bp)
        app.add_url_rule('/', endpoint='index')

        return app
