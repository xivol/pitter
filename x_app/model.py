from flask import current_app
from inflection import pluralize

from sqlalchemy.ext.declarative import declared_attr, declarative_base


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
            return session.query(cls).filter(*filters)
        else:
            return session.query(cls)

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

    @classmethod
    def add(cls, *items):
        session = cls.__make_new_session()
        if len(items) > 1:
            session.add_all(items)
        else:
            session.add(items[0])
        session.commit()
        session.close()

    @classmethod
    def remove(cls, *items):
        session = cls.__make_new_session()
        for item in items:
            session.delete(item)
        session.commit()
        session.close()

    @classmethod
    def update(cls, *items):
        session = cls.__make_new_session()
        session.commit()
        session.close()


XModel = declarative_base(cls=XModel)