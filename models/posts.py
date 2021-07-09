from datetime import datetime
from flask import current_app, url_for
from sqlalchemy import *
from sqlalchemy.orm import relation as Relation

from x_app.model import XModel
#from sqlalchemy_serializer import SerializerMixin

SHARE_OPTIONS = ['Public', 'Friends', 'Just Me']


class Post(XModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    share_options = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = Relation('User')

    def __init__(self, author_id, content, share_options=SHARE_OPTIONS[0], created=None):
        self.user_id = author_id
        self.created_date = created if created else datetime.now()
        self.update(content, share_options)

    @property
    def editable(self):
        return self.user_id == current_app.identity_provider.current_user.id

    @property
    def removable(self):
        return self.user_id == current_app.identity_provider.current_user.id

    @property
    def time_from_now(self):
        from humanize import naturaldelta
        return naturaldelta(datetime.now() - self.created_date) + ' ago'

    def update(self, content, share_options):
        self.content = content
        self.share_options = SHARE_OPTIONS.index(share_options)
