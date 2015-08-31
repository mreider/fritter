# -*- coding: utf-8 -*-

from flask import redirect, url_for
from flask.ext.login import login_required, logout_user

@login_required
def logout():
    print '>> logout'
    logout_user()
    return redirect(url_for('home'))
