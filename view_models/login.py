from flask import current_app
from werkzeug.utils import redirect

from view_models.forms.login import LoginForm
from x_app.identity_provider import XIdentityMixin
from x_app.view_model import XFormPage

from models.users import User

class LoginViewModel(XFormPage, XIdentityMixin):
    __template_name__ = 'login.html'

    def __init__(self):
        super().__init__("Login")

    def on_form_success(self, form):
        user = User.query(User.email == form.email.data).first()
        if user and current_app.identity_provider.check_password(user, form.password.data):
            current_app.identity_provider.login(user, remember=form.remember_me.data)
        return redirect(f'/user/{user.name}')

    def on_form_error(self, form):
        return super().render_template()

    def make_form(self):
        return LoginForm()
