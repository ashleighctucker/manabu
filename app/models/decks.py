from app.models.categorites import Category
from .db import db
from datetime import datetime


class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    cover_photo_url = db.Column(db.String(256))
    has_image = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        "categories.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow)

    category = db.relationship('Category', back_populates='decks')
    creator = db.relationship('User', back_populates='decks')
    cards = db.relationship('Card', back_populates='deck',
                            cascade="all, delete-orphan")
    deck_lists = db.relationship(
        'DeckList', secondary="added_decks", back_populates="decks")
    completed_users = db.relationship(
        'User', secondary="completed_decks", back_populates="completed_decks")

    @property
    def category_type(self):
        return self.category.title

    @property
    def deck_owner(self):
        return self.creator.user_name

    @property
    def cardlist(self):
        owner = str(self.creator.user_name)
        return [{'id': obj.id,
                 'title': obj.title,
                 'has_image': obj.has_image,
                 'pronunciation': obj.pronunciation,
                 'type': obj.type,
                 'definition': obj.definition,
                 'example': obj.example,
                 'image_url': obj.image_url,
                 'emoji': obj.emoji,
                 'deck_id': obj.deck_id,
                 'deck_title': self.title,
                 'deck_creator': owner
                 }
                for obj in self.cards]

    @property
    def cards_amount(self):
        return len(self.cardlist)

    @property
    def cat_color(self):
        return str(self.category.color_hex)

    def add_completed_user(self, user):
        if user not in self.completed_users:
            self.completed_users.append(user)
            return {'user': user.id}
        else:
            return {'errors': f"Deck {self.id} already in mastered by user {user.id}."}

    def remove_completed_user(self, user):
        if user in self.completed_users:
            self.completed_users.remove(user)
            return {'user': user.id}
        else:
            return {'errors': f"Could not find {user.id} in completed list"}

    def simple_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'has_image': self.has_image,
            'cover_photo_url': self.cover_photo_url,
            'category_id': self.category_id,
            'created_on': self.created_on,
            'category_id': self.category_id,
            'cards_amount': self.cards_amount,
            'color': self.cat_color
        }

    def to_dict(self):
        cat = str(self.category.title)
        owner = str(self.creator.user_name)

        return {
            'id': self.id,
            'owner_id': self.user_id,
            'title': self.title,
            'has_image': self.has_image,
            'cover_photo_url': self.cover_photo_url,
            'category': cat,
            'category_id': self.category_id,
            'creator': owner,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
            'cards': {obj.id: {'id': obj.id,
                               'title': obj.title,
                               'has_image': obj.has_image,
                               'pronunciation': obj.pronunciation,
                               'type': obj.type,
                               'definition': obj.definition,
                               'example': obj.example,
                               'image_url': obj.image_url,
                               'emoji': obj.emoji,
                               'deck_id': obj.deck_id}
                      for obj in self.cards}
        }


class DeckList(db.Model):
    __tablename__ = 'deck_lists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    has_image = db.Column(db.Boolean, default=False)
    cover_photo_url = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow)

    creator = db.relationship('User', back_populates='deck_lists')
    decks = db.relationship("Deck", secondary="added_decks",
                            back_populates="deck_lists")

    def add_deck(self, deck):
        if deck not in self.decks:
            self.decks.append(deck)
            return {'id': deck.id,
                    'title': deck.title,
                    'cover_photo_url': deck.cover_photo_url,
                    'category': deck.category_type,
                    'category_id': deck.category_id,
                    'has_image': deck.has_image,
                    'created_on': deck.created_on,
                    'cards_amount': deck.cards_amount,
                    'creator': deck.deck_owner}
        else:
            return {'errors': f"Deck {deck.title} already in list"}

    def remove_deck(self, deck):
        if deck in self.decks:
            self.decks.remove(deck)
            return {'id': deck.id}
        else:
            return {'errors': f"Could not find deck {deck.title} in list"}

    def simple_dict(self):
        return {
            'id': self.id,
            'title': self.title,
        }

    def get_cards(self):
        cards = [obj.cardlist for obj in self.decks]

        return cards

    def to_dict(self):
        owner = str(self.creator.user_name)

        return {
            'id': self.id,
            'title': self.title,
            'cover_photo_url': self.cover_photo_url,
            'creator': owner,
            'created_on': self.created_on,
            'has_image': self.has_image,
            'owner_id': self.user_id,
            'decks': {obj.id: {'id': obj.id,
                               'color': obj.cat_color,
                               'title': obj.title,
                               'cover_photo_url': obj.cover_photo_url,
                               'category': obj.category_type,
                               'category_id': obj.category_id,
                               'has_image': obj.has_image,
                               'created_on': obj.created_on,
                               'cards_amount': obj.cards_amount,
                               'creator': obj.deck_owner}
                      for obj in self.decks}
        }
