# -*- coding: utf-8 -*-

from flask import redirect, url_for, session, current_app
from flask.ext.login import current_user

def index():
    current_app.logger.info('index')

    if current_user.is_authenticated():
        current_app.logger.info('index::aready logged on')
        return redirect(url_for('home'))

    current_app.logger.info('index::login redirect')
    return redirect(url_for('login'))
