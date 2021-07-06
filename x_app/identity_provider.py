from abc import abstractmethod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user


class XIdentityProvider(LoginManager):
    def login(self, user, **options):
        login_user(user, **options)

    def logout(self):
        logout_user()

    def password_hash(self, password):
        return generate_password_hash(password)

    def check_password(self, user, password):
        return check_password_hash(user.hashed_password, password)

    @abstractmethod
    def register(self, user=None, **userdata):
        pass

    @abstractmethod
    def verify(self, user=None, **userdata):
        pass

    @abstractmethod
    def find_user(self, **userdata):
        pass

    @property
    def current_user(self):
        return current_user

    def try_login(self, **userdata):
        u = self.find_user(**userdata)
        if not u:
            return None
        if self.verify(u, **userdata):
            self.login(u, remember=userdata['remember_me'])
            return u
        return None
