from werkzeug.utils import redirect

from views.register import RegisterViewModel
from views.login import LoginViewModel
from x_app.controller import XController


class UserController(XController):
    def setup_endpoints(self):
        self.register_view_model('/register', RegisterViewModel, 'register')
        self.register_view_model('/login', LoginViewModel, 'login')
        self.register_view_func('/logout', self.logout, 'logout')

    def logout(self):
        current_app.identity_provider.logout()
        return redirect('/')
