# -*- coding: utf-8 -*-

from flask import session, render_template, redirect, url_for, current_app
from flask.ext.login import current_user, login_required, login_user
from mrsurvey.extensions import google_auth
from mrsurvey.models import User, UserWallet, Survey

@login_required
def home():
    current_app.logger.info('home')
    context = {}

    started_surveys = {wallet.survey.id: wallet for wallet in
                       UserWallet.query.filter(UserWallet.user==current_user)}
    started_surveys_ids = started_surveys.keys()

    context['surveys'] = [{
        'id': survey.id,
        'name': survey.name,
        'description': survey.description,
        'dollars': survey.dollars,
        'started': bool(started_surveys.get(survey.id, False)),
        'balance': started_surveys[survey.id].dollars if survey.id in started_surveys else 0
    } for survey in Survey.query.all()]

    return render_template('home.html', **context)
