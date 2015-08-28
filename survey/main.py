# -*- coding: utf-8 -*-

import os
from flask import Flask, session
from survey.extensions import db, oauth, google_auth, login_manager
from survey.routes import configure_routes
from survey.models import User

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

    login_manager.init_app(app)
    login_manager.login_view = '/login'

    @login_manager.user_loader
    def load_user(userid):
        result = None
        try:
            result = User.query.get(userid)
        except:
            pass

        return result

def init_blueprint(app):
    from survey.services.item_service import module as item_service
    app.register_blueprint(item_service)

    from survey.services.comment_service import module as comment_service
    app.register_blueprint(comment_service)



app = init(__name__)
