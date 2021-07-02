from abc import abstractmethod
from flask import render_template, abort
from flask.views import View
from jinja2 import TemplateNotFound


class XViewModel(View):
    __template_name__ = ''

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def render_template(self):
        try:
            return render_template(self.__template_name__, model=self)
        except TemplateNotFound:
            abort(404)

    @abstractmethod
    def dispatch_request(self):
        pass


class XPageModel(XViewModel):
    def __init__(self, title):
        self.title = title

    def dispatch_request(self):
        return self.render_template()


class XFormPage(XPageModel):
    methods = ['GET', 'POST']

    def __init__(self, title):
        super().__init__(title)
        self.form = None

    def dispatch_request(self):
        self.form = self.make_form()
        if self.form.validate_on_submit():
            return self.on_form_success(self.form)
        else:
            return self.on_form_error(self.form)

    @abstractmethod
    def make_form(self):
        pass

    @abstractmethod
    def on_form_success(self, form):
        pass

    @abstractmethod
    def on_form_error(self, form):
        pass