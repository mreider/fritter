# -*- coding: utf-8 -*-

DEBUG=True
SECRET_KEY = '0edde145198466160e02dbb9bb67e57d14e6f30929af0e7f'

SQLALCHEMY_DATABASE_URI='mysql://'

GOOGLE = {
    'consumer_key': 'from env vars',
    'consumer_secret': 'from env vars'
}

REMEMBER_COOKIE_DURATION6=3600

PLATFORM='cf' # 'heroku'