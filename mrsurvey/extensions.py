# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(session_options={'autoflush': False})

#from flask.ext.login import LoginManager
from mrsurvey.flask_login import LoginManager
login_manager = LoginManager()

from flask_oauthlib.client import OAuth
oauth = OAuth()

google_auth = oauth.remote_app(
    'google',
    app_key='GOOGLE',
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
