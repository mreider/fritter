# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import jsonify

class BaseAPI(MethodView):
    def response_ok(self, message='', data={}):
        return jsonify(**{'success': True, 'message': message, 'data': data}), 200

    def response_fail(self, message='', data={}):
        return jsonify(**{'success': False, 'message': message, 'data': data}), 200

    def response_error(self, message='', data={}):
        return jsonify(**{'success': False, 'message': message, 'data': data}), 500
