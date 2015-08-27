# -*- coding: utf-8 -*-

import os
from flask import Flask, session
from survey.common.routes import configure_routes
from survey.extensions import db, oauth, google_auth


def init(name):
    app = Flask(name)

    configure_app(app)
    configure_extensions(app)
    configure_routes(app)
    init_blueprint(app)

    return app


def configure_app(app):
    app.config.from_object('survey.config.app_config')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLEARDB_DATABASE_URL')

    if os.getenv('GOOGLE_CONSUMER_KEY') and os.getenv('GOOGLE_CONSUMER_SECRET'):
        app.config['GOOGLE']['consumer_key'] = os.getenv('GOOGLE_CONSUMER_KEY')
        app.config['GOOGLE']['consumer_secret'] = os.getenv('GOOGLE_CONSUMER_SECRET')


def configure_extensions(app):
    db.init_app(app)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

    oauth.init_app(app)

    @google_auth.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')


def init_blueprint(app):
    pass
    # TODO: Initialize AJAX service here

app = init(__name__)
