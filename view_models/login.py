from flask import current_app
from werkzeug.utils import redirect

from view_models.forms.login import LoginForm
from x_app.view_model import XFormPage


class LoginViewModel(XFormPage):
    __template_name__ = 'login.html'

    def __init__(self):
        super().__init__("Login")

    def on_form_success(self, form):
        current_app.identity_provider.login(form.email, remember_me=form.remember.me)
        return redirect(f'/user/{form.name}')

    def on_form_error(self, form):
        return super().render_template()

    def make_form(self):
        return LoginForm()
