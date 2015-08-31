# -*- coding: utf-8 -*-

from flask import redirect, url_for, get_flashed_messages, session
from flask.ext.login import current_user

def index():
    print '>> index'

    if current_user.is_authenticated():
        print '>> index.loggedon'
        get_flashed_messages()
        return redirect(url_for('home'))

    return redirect(url_for('login'))
