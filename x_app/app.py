from abc import abstractmethod
from flask import Flask
from flask_sqlalchemy_session import flask_scoped_session



class XApp(Flask):
    def __init__(self, config=None, identity=None, data=None):
        super().__init__(__class__.__name__.lower())
        if config:
            if isinstance(config, str):
                self.config.from_pyfile(config)
            else:
                self.config.from_object(config)

        if data:
            self.data_provider = data
            self.__db_scope = data.setup_scope(self)
        if identity:
            self.identity_provider = identity
            identity.init_app(app=self)

        with self.app_context():
            self.setup_data_providers()
            self.setup_identity_providers()
            self.setup_blueprints()
            self.setup_views()

    @abstractmethod
    def setup_data_providers(self):
        pass

    @abstractmethod
    def setup_identity_providers(self):
        pass

    @abstractmethod
    def setup_blueprints(self):
        pass

    @abstractmethod
    def setup_views(self):
        pass

    def start(self, **config):
        self.run(**config)
