# -*- coding: utf-8 -*-

from survey.models import *
from survey import app

with app.test_request_context():
     db.create_all()