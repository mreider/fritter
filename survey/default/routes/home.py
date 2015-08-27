# -*- coding: utf-8 -*-

from flask import session, render_template, redirect, url_for
from survey.extensions import google_auth

def home():
    if 'google_token' not in session:
        return redirect(url_for('login'))

    me = google_auth.get('userinfo')
    print me.data

    # TODO: Get email from data
    # TODO: Get userdata from database by email
    # TODO: Put itinto template

    context = {
    }

    return render_template('default/index.html', **context)
