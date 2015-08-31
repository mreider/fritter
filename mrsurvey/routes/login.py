# -*- coding: utf-8 -*-

from flask import url_for
from mrsurvey.extensions import google_auth

def login():
    print '>> login'
    return google_auth.authorize(callback=url_for('authorized', _external=True))
