# -*- coding: utf-8 -*-

from flask import request, flash, redirect, render_template
from flask.ext.login import current_user, login_required, login_user
from mrsurvey.models import User

@login_required
def survey():
    survey_id = request.args.get('survey_id')
    context = {}

    if not survey_id:
        flash('No such survey', 'error')
        return redirect('home')

    return render_template('survey.html', **context)
