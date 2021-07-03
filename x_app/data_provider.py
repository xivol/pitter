import sqlalchemy
import sqlalchemy.orm as orm

from .model import XModel

# from flask_sqlalchemy import *
# XDataProvider(SQLAlchemy)


class XDataProvider:
    def __init__(self, connection_string, echo=False):
        print(f"Подключение к базе данных по адресу {connection_string}")

        self.__engine = sqlalchemy.create_engine(connection_string, echo=echo)
        self.__session_maker = orm.sessionmaker(bind=self.__engine, expire_on_commit = False)

    def connect(self):
        return self.__session_maker()

    def create(self, model_class):
        model_class.__table__.create(bind=self.__engine, checkfirst=True)


class SQLiteDataProvider(XDataProvider):
    def __init__(self, filename, echo=False):
        if not filename or not filename.strip():
            raise ValueError("Необходимо указать имя файла базы данных.")

        conn_str = f'sqlite:///{filename.strip()}?check_same_thread=False'

        super().__init__(conn_str, echo)