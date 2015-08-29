# -*- coding: utf-8 -*-

from flask import session, render_template, redirect, url_for
from flask.ext.login import current_user, login_required, login_user
from survey.extensions import google_auth
from survey.models import User

@login_required
def home():
#    if 'google_token' not in session:
#        return redirect(url_for('login'))
#
#    me = google_auth.get('userinfo')
#
#    user = User.query.filter(User.email == me.data['email']).first()
#
#    if me and me.data and not user:
#        return redirect(url_for('logout'))

    if 'google_token' in session:
        me = google_auth.get('userinfo')

        error = me.data.get('error')
        if error:
            if error.get('code') == 401:
                return redirect(url_for('logout'))

        user = User.query.filter(User.email == me.data['email']).first()
        if user:
            login_user(user)

    context = {}
    return render_template('home.html', **context)
