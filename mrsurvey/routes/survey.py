# -*- coding: utf-8 -*-

from flask import request, flash, redirect, render_template, url_for
from flask.ext.login import current_user, login_required, login_user
from mrsurvey.models import UserWallet, Survey
from mrsurvey.extensions import db

@login_required
def survey():
    survey_id = request.args.get('survey_id')
    context = {}

    if not survey_id:
        flash('No such survey', 'error')
        return redirect('home')

    survey = Survey.query.get(survey_id)

    if not survey:
        flash('No such survey', 'error')
        return redirect(url_for('home'))

    wallet = UserWallet.query.filter(UserWallet.user==current_user).filter(UserWallet.survey_id==survey_id).first()
    if not wallet:
        wallet = UserWallet(user=current_user, survey=survey, dollars=survey.dollars)
        db.session.add(wallet)
        db.session.commit()
    context['wallet'] = wallet

    return render_template('survey.html', **context)
