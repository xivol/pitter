import datetime

from flask import current_app, url_for
from sqlalchemy import *
from sqlalchemy.orm import relation as Relation

from x_app.model import XModel
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(XModel, UserMixin, SerializerMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, unique=True,)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)

    first_name = Column(String)
    last_name = Column(String, default='')
    description = Column(String, nullable=True)
    profile_image = Column(String, default='profile-icon.svg')

    posts = Relation('Post', back_populates='user')

    def __init__(self, username, email, password_hash, first_name, last_name=None, about=None):
        self.first_name = first_name
        self.last_name = last_name
        self.description = about
        self.username = username
        self.email = email
        self.hashed_password = password_hash

    def __repr__(self):
        return f'<User> {self.id} {self.username}'

    @property
    def profile_image_url(self):
        return url_for('static', filename=f'profile/{self.profile_image}')

    @property
    def can_post(self):
        cu = current_app.identity_provider.current_user
        return cu.is_authenticated and self.id == cu.id
