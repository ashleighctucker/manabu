from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    has_image = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow)

    decks = db.relationship(
        'Deck', back_populates='creator', cascade="all, delete-orphan")
    cards = db.relationship(
        'Card', back_populates='creator', cascade="all, delete-orphan")
    deck_lists = db.relationship(
        'DeckList', back_populates='creator',  cascade="all, delete-orphan")
    completed_decks = db.relationship(
        'Deck', secondary="completed_decks", back_populates='completed_users')
    badges = db.relationship(
        'Badge', secondary="user_badges", back_populates="users")

    @property
    def password(self):
        return self.hashed_password

    @property
    def decks_list(self):
        return [{'id': deck.id,
                 'title': deck.title,
                 'category_id': deck.category_id,
                 'created_on': deck.created_on, } for deck in self.decks]

    @property
    def lists_list(self):
        return [{'id': decklist.id,
                 'title': decklist.title} for decklist in self.deck_lists]

    @property
    def badge_dict(self):
        return {badge.id: {'id': badge.id, 'title': badge.title} for badge in self.badges}

    @property
    def completed_dict(self):
        return {obj.id: {'deck_id': obj.id, 'created_on': obj.created_on} for obj in self.completed_decks}

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.user_name,
            'email': self.email,
            'first_name': self.first_name,
            'created_on': self.created_on,
            'decks': self.decks_list,
            'lists': self.lists_list,
            'completed_decks': self.completed_dict,
            'badges': self.badge_dict
        }
