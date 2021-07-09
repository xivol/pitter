from flask import current_app, url_for, flash
from werkzeug.utils import redirect

from view_models.forms.login import LoginForm
from x_app.identity_provider import WrongPasswordError, UserNotFoundError
from x_app.navigation import XNavigationMixin, XNav
from x_app.view_model import XFormPage


class LoginViewModel(XFormPage, XNavigationMixin):
    __template_name__ = 'login.html'

    def __init__(self):
        super().__init__("Sign In")

    def on_form_success(self, form):
        try:
            u = current_app.identity_provider.try_login(**form.get_user_data())
            return redirect(f'/user/{u.username}')
        except WrongPasswordError:
            flash('User and password doesn\'t match!', 'danger')
            return self.on_form_error(form)
        except UserNotFoundError:
            flash('User is not found!', 'danger')
            return self.on_form_error(form)

    def on_form_error(self, form):
        return super().render_template()

    def make_form(self):
        return LoginForm()

    @property
    def navigation(self):
        return [XNav('Sign Up', url_for('auth.register'), 'btn-light')]
