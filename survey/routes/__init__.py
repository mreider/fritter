# -*- coding: utf-8 -*-

from flask import send_from_directory
from survey.config import settings
import importlib


def configure_routes(app):
    for module_name, module_config in settings.ROUTES.items():
        module = importlib.import_module('survey.{}'.format(module_name))

        endpoint = getattr(module, module_config['endpoint'])

        app.add_url_rule(
            module_config['route'],
            module_config['endpoint'],
            endpoint,
            methods=module_config['methods']
        )


    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')
