# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from survey.extensions import db
from survey.services.base import BaseAPI
from survey.models import Item, User, Purchase
from datetime import datetime

module = Blueprint('service.item_service', __name__)

class ItemAPI(BaseAPI):
    decorators = [login_required]

    def get(self):
        # TODO: Add sort: "sorted by dollars spent in users_items - descending, and price - descending"
        items = Item.query.all()
        purchased = [p.thing_id for p in current_user.purchases]

        serialzied_items = [{
            'name': item.name,
            'description': item.description,
            'id': item.id,
            'price': item.price,
            'purchased': item.id in purchased,
            'comments_count': len(item.comments)
        } for item in items]

        return self.response_ok(data={'items': serialzied_items})

    def post(self):
        action = request.json.get('action')
        item_id = request.json.get('item_id')

        if action == 'buy':
            item = Item.query.get(item_id)

            if current_user.dollars < item.price:
                return self.response_fail('You do not have enough dollars')
            else:
                current_user.dollars -= item.price
                purchase = Purchase(
                    user=current_user,
                    thing=item,
                    dollars=item.price,
                    bought_date=datetime.utcnow()
                )

                db.session.add(purchase)
                db.session.commit()

                who = [{'name': p.user.name, 'avatar': p.user.avatar}
                       for p in Purchase.query
                       .filter(Purchase.thing_id==item_id)
                       .filter(Purchase.user!=current_user).all()]

                return self.response_ok(data={
                    'purchase': purchase.serialize(),
                    'who_bought': who
                })
        elif action == 'sell':
            purchase = Purchase.query.filter(Purchase.thing_id==item_id).filter(Purchase.user==current_user).first()

            if not purchase:
                return self.response_fail('You do not have this thing')
            else:
                current_user.dollars += purchase.dollars

                data = self.response_ok(data={
                    'user': current_user.serialize(),
                    'item_id': item_id,
                    'purchase': purchase.serialize()
                })

                db.session.delete(purchase)
                db.session.commit()

                return data

        return self.response_fail('Wrong method')


service_item_view = ItemAPI.as_view('service_item_view')
module.add_url_rule(
    '/service/item_service/',
    view_func=service_item_view,
    methods=['POST', 'GET']
)
