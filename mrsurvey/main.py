# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask, session, json
from mrsurvey.extensions import db, oauth, google_auth, login_manager
from mrsurvey.routes import configure_routes
from mrsurvey.models import User

def init(name):
    app = Flask(name)

    configure_app(app)
    configure_extensions(app)
    configure_routes(app)
    init_blueprint(app)

    return app


def configure_app(app):
    app.config.from_object('mrsurvey.config.app_config')

    platform = os.getenv('PLATFORM', app.config['PLATFORM'])

    if not platform:
        raise ValueError('PLATFORM must be defined either through config or through environment variable')

    app.config['PLATFORM'] = platform

    if app.config['PLATFORM'] == 'heroku':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLEARDB_DATABASE_URL')
    elif app.config['PLATFORM'] == 'cf':
        vcap = json.loads(os.environ['VCAP_SERVICES'])
        svc = vcap['cleardb'][0]['credentials']

        uriadd = svc["uri"]

        if uriadd.endswith('?reconnect=true'):
            uriadd = uriadd[:-15]

        app.config['SQLALCHEMY_DATABASE_URI'] = uriadd

    if os.getenv('GOOGLE_CONSUMER_KEY') and os.getenv('GOOGLE_CONSUMER_SECRET'):
        app.config['GOOGLE']['consumer_key'] = os.getenv('GOOGLE_CONSUMER_KEY')
        app.config['GOOGLE']['consumer_secret'] = os.getenv('GOOGLE_CONSUMER_SECRET')
    else:
        raise ValueError('GOOGLE key/secret must be defined')

    app.logger.setLevel(logging.DEBUG)

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
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(userid):
        result = None
        try:
            result = User.query.get(int(userid))
        except:
            pass

        return result

def init_blueprint(app):
    from mrsurvey.services.item_service import module as item_service
    app.register_blueprint(item_service)

    from mrsurvey.services.comment_service import module as comment_service
    app.register_blueprint(comment_service)



app = init(__name__)
