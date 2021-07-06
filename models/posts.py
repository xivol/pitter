from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relation as Relation

from x_app.model import XModel
from sqlalchemy_serializer import SerializerMixin

SHARE_OPTIONS = ['Public', 'Friends', 'Just Me']


class Post(XModel, SerializerMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    share_options = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = Relation('User')

    def __init__(self, author_id, content, share_options=SHARE_OPTIONS[0], created=datetime.now()):
        self.user_id = author_id
        self.content = content
        self.share_options = SHARE_OPTIONS.index(share_options)
        self.created_date = created

