# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, session
from survey.extensions import google_auth
from flask_oauthlib.client import OAuthException

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
        me = google_auth.get('userinfo')
        print me.data

        # TODO: Check if user not in database, then put him into DB
        """
        "data": {
        "email": "nosuchip@gmail.com",
        "family_name": "Popov",
        "gender": "other",
        "given_name": "Alex",
        "id": "118253614024394073502",
        "link": "https://plus.google.com/118253614024394073502",
        "name": "Alex Popov",
        "picture": "https://lh5.googleusercontent.com/-qWuu9o6zrio/AAAAAAAAAAI/AAAAAAAAEU4/SadfGpGGqZM/photo.jpg",
        "verified_email": true
        }
        """

    return redirect(url_for('home'))
