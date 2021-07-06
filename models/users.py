import datetime
from sqlalchemy import *
from sqlalchemy.orm import relation as Relation
from werkzeug.security import generate_password_hash, check_password_hash

from x_app.model import XModel
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(XModel, UserMixin, SerializerMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)

    posts = Relation("Post", back_populates='user')

    def __init__(self, username, email, password_hash, first_name, last_name=None, about=None):
        self.first_name = first_name
        self.last_name = last_name
        self.description = about
        self.username = username
        self.email = email
        self.hashed_password = password_hash

    def __repr__(self):
        return f'<User> {self.id} {self.username}'