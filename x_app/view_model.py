from abc import abstractmethod
from flask import render_template, abort, request, current_app
from flask.views import View
from jinja2 import TemplateNotFound


class XViewModel(View):
    __template_name__ = ''
    __request_params__ = set()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def render_template(self):
        try:
            return render_template(self.__template_name__, model=self)
        except TemplateNotFound:
            return abort(404)

    def parse_params(self, request_kwargs):
        for param in self.__request_params__:
            self[param] = request_kwargs.get(param)

    def dispatch_request(self, *args, **kwargs):
        self.parse_params(kwargs)
        return self.on_request(request)

    @abstractmethod
    def on_request(self, request):
        pass


class XPageModel(XViewModel):
    def __init__(self, title):
        self.title = title

    def on_request(self, request):
        return self.render_template()


class XFormPage(XPageModel):
    methods = ['GET', 'POST']

    def __init__(self, title):
        super().__init__(title)
        self.form = None

    def on_request(self, request):
        self.form = self.make_form()
        if request.method == 'POST':
            if self.form.validate_on_submit():
                return self.on_form_success(self.form)
            else:
                return self.on_form_error(self.form)
        else:
            return super().render_template()

    @abstractmethod
    def make_form(self):
        pass

    @abstractmethod
    def on_form_success(self, form):
        pass

    @abstractmethod
    def on_form_error(self, form):
        pass