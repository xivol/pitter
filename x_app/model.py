from flask import current_app
from inflection import pluralize

from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy import func

class XModel(object):

    @declared_attr
    def __tablename__(cls):
        return pluralize(cls.__name__.lower())

    @classmethod
    def setup_table(cls):
        current_app.data_provider.create(cls)

    @classmethod
    def __make_new_session(cls):
        return current_app.data_provider.connect()

    @classmethod
    def query(cls, *filters):
        session = cls.__make_new_session()
        if len(filters):
            return session.query(cls).autoflush(False).filter(*filters)
        else:
            return session.query(cls).autoflush(False)

    @classmethod
    def all(cls):
        return cls.query().all()

    @classmethod
    def get(cls, pk):
        return cls.query().get(pk)

    @classmethod
    def find(cls):
        return cls.query().filter()

    @classmethod
    def count(cls):
        session = cls.__make_new_session()
        return session.query(func.count('*')).select_from(cls).scalar()


XModel = declarative_base(cls=XModel)