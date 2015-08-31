# -*- coding: utf-8 -*-

from flask import session, redirect, url_for

def logout():
    session.pop('google_token', None)
    return redirect(url_for('home'))
