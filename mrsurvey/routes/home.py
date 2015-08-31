# -*- coding: utf-8 -*-

from flask import session, render_template, redirect, url_for
from flask.ext.login import current_user, login_required, login_user
from mrsurvey.extensions import google_auth
from mrsurvey.models import User, UserWallet, Survey

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

    context = {}

    # DO NOT COMMIT!
    import pdb; pdb.set_trace();
    # DO NOT COMMIT!

    if 'google_token' in session:
        me = google_auth.get('userinfo')

        error = me.data.get('error')
        if error:
            if error.get('code') == 401:
                return redirect(url_for('logout'))

        user = User.query.filter(User.email == me.data['email']).first()
        if user:
            login_user(user)

    started_surveys = [wallet.mrsurvey.serialize() for wallet in
                       UserWallet.query.filter(UserWallet.user==current_user)]
    started_surveys_ids = [s.id for s in started_surveys]

    context['surveys'] = [{
        'id': survey.id,
        'name': survey.name,
        'description': survey.description,
        'dollars': survey.dollars,
        'started': survey.id in started_surveys_ids,
        'balance': started_surveys[survey.id].wallet.dollars if survey.id in started_surveys_ids else 0,
    } for survey in Survey.query.all()]

    return render_template('home.html', **context)
