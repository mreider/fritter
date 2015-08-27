# -*- coding: utf-8 -*-

from flask import url_for
from survey.extensions import google_auth

def login():
    return google_auth.authorize(callback=url_for('authorized', _external=True))
