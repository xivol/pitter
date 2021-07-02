import datetime
from sqlalchemy import *
from sqlalchemy.orm import relation as Relation
from werkzeug.security import generate_password_hash, check_password_hash

from x_app.model import XModel
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(XModel, UserMixin, SerializerMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    about = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)

    news = Relation("News", back_populates='user')

    def __init__(self, name, about, email, password_hash):
        self.name = name
        self.about = about
        self.email = email
        self.hashed_password = password_hash

    def __repr__(self):
        return f'<User> {self.id} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)