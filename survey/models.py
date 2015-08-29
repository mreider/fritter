# -*- coding: utf-8 -*-

from survey.extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    avatar = db.Column(db.String(200))
    dollars = db.Column(db.Integer, default=100)
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
#            'dollars': self.dollars,
            'id': self.id
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String)
    price = db.Column(db.Integer)
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
                'dollars': self.user.dollars,
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
