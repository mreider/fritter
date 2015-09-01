# -*- coding: utf-8 -*-

import os
from flask import Flask, session, json
from mrsurvey.extensions import db, oauth, google_auth, login_manager
from mrsurvey.routes import configure_routes
from mrsurvey.models import User

vcap = json.loads(os.environ['VCAP_SERVICES'])
svc = vcap['cleardb'][0]['credentials']
# host=svc["hostname"]
# port=svc["port"]
# password=svc["password"]
# username=svc["username"]
# name=svc["name"]
# uri=svc["uri"]

def init(name):
    app = Flask(name)

    configure_app(app)
    configure_extensions(app)
    configure_routes(app)
    init_blueprint(app)

    return app


def configure_app(app):
    app.config.from_object('mrsurvey.config.app_config')
    uriadd = svc["uri"]
    if uriadd.endswith('?reconnect=true'):
      uriadd = uriadd[:-15] 
    app.config['SQLALCHEMY_DATABASE_URI'] = uriadd

    app.config['GOOGLE']['consumer_key'] = "335264890335-0lm8m9jus0p7h7186iu22dlevkqbqtgo.apps.googleusercontent.com"
    app.config['GOOGLE']['consumer_secret'] = "Jr38yO8jvuymtkYxvpruOoKK"


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
