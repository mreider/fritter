# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from mrsurvey.extensions import db
from mrsurvey.services.base import BaseAPI
from mrsurvey.models import Item, User, Purchase, UserWallet, Survey
from datetime import datetime

module = Blueprint('service.item_service', __name__)

class ItemAPI(BaseAPI):
    decorators = [login_required]

    def get(self):
        action = request.args.get('action');
        survey_id = int(request.args.get('survey_id', -1))

        if action == 'wallet':
            survey = Survey.query.filter(Survey.id==survey_id).first()

            if not survey:
                return self.response_fail(message='Survey not found')

            wallet = UserWallet.query.filter(UserWallet.user==current_user).filter(UserWallet.survey_id==survey_id).first()
            if not wallet:
                wallet = UserWallet(user=current_user, survey=survey, dollars=survey.dollars)
                db.session.add(wallet)
                db.session.commit()

            return self.response_ok(data={'wallet': wallet.serialize()})

        serialized_items = []

        items = Item.query.select_from(Item).filter(Item.survey_id==survey_id).all()
        purchased = [p.thing_id for p in current_user.purchases if p.thing.survey_id==survey_id]
        for item in items:
            item_dict = {
                'name': item.name,
                'description': item.description,
                'id': item.id,
                'price': item.price,
                'purchased': item.id in purchased,
                'comments_count': len(item.comments),
                'who_bought': [{'name': p.user.name, 'avatar': p.user.avatar}
                               for p in Purchase.query
                               .filter(Purchase.thing_id==item.id)
                               .filter(Purchase.user!=current_user).all()]
            }
            serialized_items.append(item_dict)

        return self.response_ok(data={'items': serialized_items})

    def post(self):
        action = request.json.get('action')
        item_id = int(request.json.get('item_id'))
        survey_id = int(request.json.get('survey_id'))

        if action == 'buy':
            item = Item.query.get(item_id)
            wallet = UserWallet.query.filter(UserWallet.user==current_user).filter(UserWallet.survey_id==survey_id).one()

            if wallet.dollars < item.price:
                return self.response_fail('You do not have enough dollars')
            else:
                wallet.dollars -= item.price
                purchase = Purchase(
                    user=current_user,
                    thing=item,
                    dollars=item.price,
                    bought_date=datetime.utcnow()
                )

                db.session.add(purchase)
                db.session.commit()

                return self.response_ok(data={
                    'purchase': purchase.serialize(),
                    'balance': wallet.dollars
                })
        elif action == 'sell':
            purchase = (Purchase.query
                        .filter(Purchase.thing_id==item_id)
                        .filter(Purchase.user==current_user)
                        .one())

            if not purchase:
                return self.response_fail('You do not have this thing')
            else:
                wallet = (UserWallet.query
                          .filter(UserWallet.user==current_user)
                          .filter(UserWallet.survey_id==survey_id)
                          .one())
                wallet.dollars += purchase.dollars

                data = self.response_ok(data={
                    'user': current_user.serialize(),
                    'item_id': item_id,
                    'purchase': purchase.serialize(),
                    'balance': wallet.dollars
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
