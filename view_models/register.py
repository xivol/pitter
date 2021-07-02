from flask import current_app
from werkzeug.utils import redirect
from .forms.register import RegisterForm
from x_app.view_model import XFormPage


class RegisterViewModel(XFormPage):
    __template_name__ = 'register.html'

    def __init__(self):
        super().__init__("Register")

    def make_form(self):
        return RegisterForm()

    def on_form_success(self, form):
        current_app.identity_provider.register(
            name=form.name,
            email=form.email,
            about=form.about,
            password=form.password
        )
        return redirect(f'/user/{form.name}')

    def on_form_error(self, form):
        return self.render_template()
