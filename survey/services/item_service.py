# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from survey.extensions import db
from survey.models import Item, User, Purchase
from datetime import datetime

module = Blueprint('service.item_service', __name__)

class ItemAPI(MethodView):
    decorators = [login_required]

    def post(self, action, item_id):
        response = {'success': True, 'message': '', data: {}}

        if action == 'buy':
            item = Items.query.get(item_id)

            if current_user.dollars < item.price:
                response['success'] = False
                response['message'] = 'You do not have enough dollars'
            else:
                user.dollars -= item.price
                purchase = Purchase(
                    user=user,
                    thing=item,
                    dollars=item.price,
                    bought_date=datetime.utcnow()
                )

                db.session.add(purchase)

                response['data'] = {
                    'purchase': {
                        'dollars': purchase.dollars,
                        'bought_date': item.bought_date,
                        'user': {
                            'email': user.email,
                            'dollars': user.dollars,
                            'id': user.id
                        },
                        'item': {
                            'name': item.name,
                            'description': item.description,
                            'id': item.id
                        }
                    }
                }

                db.session.commit()
        elif action == 'sell':
            purchase = Purchase.query.filter(Purchase.thing.id==item_id).filter(Purchase.user==current_user).first()

            if not purchase:
                response['success'] = False
                response['message'] = 'You do not have this thing'
            else:
                user.dollars += pruchase.dollars
                db.session.delete(purchase)

                response['data'] = {
                    'user': {
                        'email': user.email,
                        'dollars': user.dollars,
                        'id': user.id
                    },
                    'item_id': item_id,
                    'purchase_to_remove': {
                        'dollars': purchase.dollars,
                        'bought_date': item.bought_date,
                        'item': {
                            'name': item.name,
                            'description': item.description,
                            'id': item.id
                        }
                    }
                }

                db.session.commit()
        else:
            response = {'success': False, 'message': 'Wrong method'}

        return jsonify(response)


service_item_view = ItemAPI.as_view('service_item_view')
module.add_url_rule('/service/item_service/<action>/<item_id>', view_func=service_item_view, methods=['POST', ])
