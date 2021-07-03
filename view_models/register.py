from flask import current_app
from werkzeug.utils import redirect

from view_models.forms.register import RegisterForm
from x_app.identity_provider import XIdentityMixin
from x_app.view_model import XFormPage


class RegisterViewModel(XFormPage, XIdentityMixin):
    __template_name__ = 'register.html'

    def __init__(self):
        super().__init__("Sign Up")

    def make_form(self):
        return RegisterForm()

    def on_form_success(self, form):
        current_app.identity_provider.register(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            password=form.password.data
        )
        return redirect(f'/user/{form.name.data}')

    def on_form_error(self, form):
        return self.render_template()

