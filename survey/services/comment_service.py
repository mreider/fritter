# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from survey.extensions import db
from survey.models import Item, User, Purchase
from datetime import datetime

module = Blueprint('service.comment_service', __name__)

class CommentAPI(MethodView):
    decorators = [login_required]

    def get(self, item_id):
        response = {'success': True, 'message': '', data: {}}


        return jsonify(response)

    def post(self, item_id):
        response = {'success': True, 'message': '', data: {}}


        return jsonify(response)


service_comment_view = CommentAPI.as_view('service_comment_view')
module.add_url_rule('/service/comment_service/<item_id>', view_func=service_comment_view, methods=['POST', 'GET'])
