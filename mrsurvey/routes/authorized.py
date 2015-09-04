# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, session, current_app, render_template
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
        try:
            session['google_token'] = (response['access_token'], '')

            me = google_auth.get('userinfo') or {}

            if current_app.config['LIMIT_DOMAINS']:
                username, domain = me.data['email'].split('@')
                if domain not in current_app.config['LIMIT_DOMAINS']:
                    if 'token' in session:
                        session.pop('token')

                    return render_template('domain_denied.html',
                                           allowed_domains=current_app.config['LIMIT_DOMAINS'],
                                           denied_domain=domain,
                                           email=me.data['email'].split('@'))

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

        except Exception as ex:
            current_app.logger.error('AUTHORIZED: Exception occurs: "{}"'.format(ex))

    return redirect(url_for('home'))
