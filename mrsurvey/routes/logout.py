# -*- coding: utf-8 -*-

from flask import redirect, url_for, current_app
from flask.ext.login import login_required, logout_user

@login_required
def logout():
    current_app.logger.info('logout')
    logout_user()
    return redirect(url_for('index'))
