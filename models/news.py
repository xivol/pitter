from datetime import datetime

from flask import current_app
from sqlalchemy import *
from sqlalchemy.orm import relation as Relation

from x_app.model import XModel
from sqlalchemy_serializer import SerializerMixin


class News(XModel, SerializerMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.now)
    is_private = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = Relation('User')

    def __init__(self, author, title, content, is_private=True, created=datetime.now()):
        self.user_id = author.id
        self.title = title
        self.content = content
        self.is_private = is_private
        self.created_date = created