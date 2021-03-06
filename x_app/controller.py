from abc import abstractmethod

from flask_login import login_required
from inflection import underscore
import flask


class XController:
    def __init__(self, **blueprint_config):
        self.__bp = flask.Blueprint(
            self.__class__.blueprint_name(),
            __name__,
            **blueprint_config
        )
        self.setup_endpoints()

    @classmethod
    def blueprint_name(cls):
        bp_name = cls.__name__
        if bp_name.endswith('Controller'):
            bp_name = bp_name[:-len('Controller')]
        return underscore(bp_name)

    @abstractmethod
    def setup_endpoints(self):
        pass

    def register_view_model(self, rule, view_model, endpoint, **config):
        model_config = {}
        if 'model_config' in config:
            model_config = config.pop('model_config')

        protect = False
        if 'login_required' in config:
            protect = config.pop('login_required')

        if protect:
            vf = login_required(view_model.as_view(endpoint, **model_config))
        else:
            vf = view_model.as_view(endpoint, **model_config)

        self.__bp.add_url_rule(rule, view_func=vf, **config)

    def register_view_func(self, rule, view_func, endpoint, **config):
        self.__bp.add_url_rule(rule,
                               view_func=view_func,
                               endpoint=endpoint,
                               **config)

    def register_in_app(self, application, **config):
        application.register_blueprint(self.__bp, **config)

    @classmethod
    def add_to_app(cls, app, **config):
        c = cls()
        c.register_in_app(app, **config)
