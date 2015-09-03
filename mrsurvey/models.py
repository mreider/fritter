# -*- coding: utf-8 -*-

from mrsurvey.extensions import db
from datetime import datetime


class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    dollars = db.Column(db.Integer, default=100)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'dollars': self.dollars
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    avatar = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()

    def get_id(self):
        return unicode(self.id)

    def serialize(self):
        return {
            'email': self.email,
            'avatar': self.avatar,
            'name': self.name,
            'id': self.id
        }


class UserWallet(db.Model):
    __tablename__ = 'users_wallets'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', backref='wallets')
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), primary_key=True)
    survey = db.relationship('Survey')
    dollars = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'survey_id': self.survey_id,
            'dollars': self.dollars
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String)
    price = db.Column(db.Integer)

    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    survey = db.relationship('Survey', backref='items')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price
        }


class Purchase(db.Model):
    __tablename__ = 'items_users'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', backref='purchases')
    thing_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    thing = db.relationship('Item', backref='purhases')
    dollars = db.Column(db.Integer)
    bought_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'dollars': self.dollars,
            'bought_date': self.bought_date.strftime('%Y-%m-%d %H:%M:%S'),
            'user': {
                'email': self.user.email,
                'avatar': self.user.avatar,
                'name': self.user.name,
            },
            'item': self.thing.serialize()
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', cascade='all', backref='comments')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('Item', cascade='all', backref='comments')
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'item': self.item.serialize(),
            'comment': self.comment,
            'posted': self.posted.strftime('%Y-%m-%d %H:%M:%S'),
        }
