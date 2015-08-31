# -*- coding: utf-8 -*-

import yaml
from flask import session, render_template, url_for, request
from StringIO import StringIO
from mrsurvey.models import Survey, Item
from datetime import datetime
from mrsurvey.extensions import db


def loadyaml():
    context = {'errors': []}

    if request.method == 'POST':
        yaml_file = request.files['yaml']
        if yaml_file and yaml_file.filename.endswith('yml'):
            buffer = StringIO()
            yaml_file.save(buffer)
            data = yaml.load(buffer.getvalue())

            if data.get('name') and data.get('dollars') and data.get('items') and len(data.get('items')):
                survey = Survey(
                    name=data['name'],
                    description=data['description'],
                    dollars=data['dollars'],
                    created_date=datetime.utcnow()
                )

                for item in data['items']:
                    item = Item(name=item['name'], description=item['description'], price=item['price'])
                    db.session.add(item)
                    survey.items.append(item)

                db.session.add(survey)
                db.session.commit()
            else:
                context['errors'].append('Missing one of required fields: "name", "dollars", "items"')

    return render_template('loadyaml.html', **context)
