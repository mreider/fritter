# -*- coding: utf-8 -*-

from flask import url_for, current_app
from mrsurvey.extensions import google_auth

def login():
    current_app.logger.info('login')
    return google_auth.authorize(callback=url_for('authorized', _external=True))
