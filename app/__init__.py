#!/usr/bin/env python3
from flask import ( Flask, render_template, flash, g )
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
            if g.user is None:
                return render_template("index.html")
            if g.user["events_id"] is None or len(g.user["events_id"]) == 0:
                return render_template("user-homepage.html", posts=[])
            from .events import ( get_post )
            events_ids = g.user["events_id"].split(",")
            events = []
            for e in events_ids:
                events.append(get_post(int(e)))

            return render_template("user-homepage.html", posts=events)

        from . import db
        db.init_app(app)

        from . import auth
        app.register_blueprint(auth.bp)

        from . import events
        app.register_blueprint(events.bp)
        # app.add_url_rule('/', endpoint='index')

        return app
