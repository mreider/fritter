# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, session, current_app
from flask_oauthlib.client import OAuthException
from flask.ext.login import login_user
from mrsurvey.extensions import db, google_auth
from mrsurvey.models import User

def authorized():
    current_app.logger.info('authorized')

    response = google_auth.authorized_response()

    if response is None:
        flash('Access denied: reason={} error={}'.format(
            request.args.get('error_reason', 'no reason'),
            request.args.get('error_description', 'no description')
        ), 'error')
        return redirect(url_for('logout'))
    elif type(response) == OAuthException:
        current_app.logger.error('OAuthException: "{}: {}"'.format(
            response.message,
            response.data.get('error_description') if response.data else 'no descriptio'))
        return redirect(url_for('logout'))
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
