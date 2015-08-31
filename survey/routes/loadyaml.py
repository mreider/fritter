# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request
import yaml
from StringIO import StringIO

def loadyaml():
    if request.method == 'POST':
        yaml = request.files['yaml']
        if yaml and yaml.filename.endswith('yml'):
            buffer = StringIO()
            yaml.save(buffer)
            data = yaml.load(buffer.getvalue())

    return render_template('loadyaml.html')
