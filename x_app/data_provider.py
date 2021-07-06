import sqlalchemy
import sqlalchemy.orm as orm


class XDataProvider:
    def __init__(self, connection_string, echo=False):
        print(f"Подключение к базе данных по адресу {connection_string}")

        self.__engine = sqlalchemy.create_engine(connection_string, echo=echo)
        self.__session_maker = orm.sessionmaker(bind=self.__engine, expire_on_commit = False)

    def connect(self):
        return self.__session_maker()

    def create(self, model_class):
        model_class.__table__.create(bind=self.__engine, checkfirst=True)

    def add(self, *items):
        session = self.connect()
        if len(items) > 1:
            session.add_all(items)
        else:
            session.add(items[0])
        session.commit()
        session.close()

    def remove(self, *items):
        session = self.connect()
        for item in items:
            session.delete(item)
        session.commit()
        session.close()

    def update(self, *items):
        session = self.connect()
        session.commit()
        session.close()


class SQLiteDataProvider(XDataProvider):
    def __init__(self, filename, echo=False):
        if not filename or not filename.strip():
            raise ValueError("Необходимо указать имя файла базы данных.")

        conn_str = f'sqlite:///{filename.strip()}?check_same_thread=False'

        super().__init__(conn_str, echo)