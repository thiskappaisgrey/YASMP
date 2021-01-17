#!/usr/bin/env python3
from flask import ( Flask, render_template )
# from flask_sqlalchemy import SQLAlchemy



def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    # db.init_app(app)

    with app.app_context():
        @app.route('/')
        def index():
            return render_template("index.html")

        from . import db
        db.init_app(app)

        from . import auth
        app.register_blueprint(auth.bp)

        from . import events
        app.register_blueprint(events.bp)
        # app.add_url_rule('/', endpoint='index')

        return app
