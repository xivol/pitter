from flask import current_app, url_for
from werkzeug.utils import redirect

from view_models.forms.login import LoginForm
from x_app.navigation import XNavigationMixin, XNav
from x_app.view_model import XFormPage

from models.users import User


class LoginViewModel(XFormPage, XNavigationMixin):
    __template_name__ = 'login.html'

    def __init__(self):
        super().__init__("Sign In")

    def on_form_success(self, form):
        if current_app.identity_provider.try_login(**form.get_user_data()):
            return redirect(f'/user/{form.username.data}')
        else:
            self.on_form_error(form)

    def on_form_error(self, form):
        return super().render_template()

    def make_form(self):
        return LoginForm()

    @property
    def navigation(self):
        return [XNav('Sign Up', url_for('auth.register'), 'btn-outline-primary')]
