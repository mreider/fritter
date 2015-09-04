# -*- coding: utf-8 -*-

from flask import redirect, url_for, current_app, get_flashed_messages, session
#from flask.ext.login import logout_user
from flask.ext.login import logout_user

def logout():
    current_app.logger.info('logout')
    if 'google_token' in session:
        session.pop('google_token')
    get_flashed_messages()
    logout_user()
    return redirect(url_for('index'))
