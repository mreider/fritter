# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.ext.login import login_required, current_user
from sqlalchemy import desc
from mrsurvey.services.base import BaseAPI
from mrsurvey.extensions import db
from mrsurvey.models import Comment, Item
from datetime import datetime

module = Blueprint('service.comment_service', __name__)

class CommentAPI(BaseAPI):
    decorators = [login_required]

    def get(self):
        item_id = int(request.args.get('item_id'))
        survey_id = int(request.args.get('survey_id'))

        if item_id:
            comments = (Comment.query
                .filter(Comment.item_id==item_id)
                .order_by(Comment.posted).all())
            return self.response_ok(data={
                'comments': [comment.serialize() for comment in comments]
            })

        return self.response_fail('Missing item')

    def post(self):
        text = request.json.get('comment')
        item_id = int(request.json.get('item_id'))
        survey_id = int(request.json.get('survey_id'))

        if text:
            comment = Comment(
                user=current_user,
                item_id=item_id,
                comment=text,
                posted=datetime.utcnow(),
                created_date=datetime.utcnow()
            )
            db.session.add(comment)
            db.session.commit()

            return self.response_ok(data={'comment': comment.serialize()})

        return self.response_fail('Missing comment')


service_comment_view = CommentAPI.as_view('service_comment_view')
module.add_url_rule(
    '/service/comment_service/',
    view_func=service_comment_view,
    methods=['POST', 'GET']
)
