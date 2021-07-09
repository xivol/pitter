import sqlalchemy
import sqlalchemy.orm as orm
from flask_sqlalchemy_session import flask_scoped_session


class XDataProvider:
    def __init__(self, connection_string, echo=False):
        # print(f"Подключение к базе данных по адресу {connection_string}")
        self.__engine = sqlalchemy.create_engine(connection_string, echo=echo)
        self.__session_maker = orm.sessionmaker(bind=self.__engine)

    def init_app(self, app):
        return flask_scoped_session(self.__session_maker, app=app)

    def connect(self):
        return self.__session_maker()

    def create(self, model_class):
        model_class.__table__.create(bind=self.__engine, checkfirst=True)

    def add(self, *items):
        session = self.connect()
        try:
            if len(items) > 1:
                session.add_all(items)
            else:
                session.add(items[0])
            session.commit()
        finally:
            session.close()

    def remove(self, *items):
        session = self.connect()
        try:
            for item in items:
                session.delete(item)
            session.commit()
        finally:
            session.close()