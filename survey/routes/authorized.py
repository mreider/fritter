# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, session
from flask_oauthlib.client import OAuthException
from flask.ext.login import login_user
from survey.extensions import db, google_auth
from survey.models import User

def authorized():
    response = google_auth.authorized_response()

    if response is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ), 'error')
    elif type(response) == OAuthException:
        flash('Error occures while redirecting after login', 'error')
    else:
        session['google_token'] = (response['access_token'], '')
        me = google_auth.get('userinfo') or {}

        user = User.query.filter(User.email == me.data['email']).first()

        if not user:
            user = User(
                name=' '.join((me.data['given_name'], me.data['family_name'])),
                email=me.data['email'],
                avatar=me.data['picture']
            )

            db.session.add(user)
            db.session.commit()

        login_user(user, remember=True)

    return redirect(url_for('home'))
