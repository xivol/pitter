from flask import current_app, url_for
from werkzeug.utils import redirect

from view_models.forms.register import RegisterForm
from x_app.navigation import XNav, XNavigationMixin
from x_app.view_model import XFormPage


class RegisterViewModel(XFormPage, XNavigationMixin):
    __template_name__ = 'register.html'

    def __init__(self):
        super().__init__("Sign Up")

    def make_form(self):
        return RegisterForm()

    def on_form_success(self, form):
        try:
            current_app.identity_provider.register(**form.get_user_data())
        except:
            self.on_form_error(form)
        return redirect(f'/user/{form.username.data}')

    def on_form_error(self, form):
        return self.render_template()

    @property
    def navigation(self):
        return [XNav('Sign In', url_for('auth.login'), 'btn-outline-primary')]


