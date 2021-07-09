from flask import current_app

from x_app.app import XApp
from x_app.data_provider import XDataProvider
from x_app.identity_provider import XIdentityProvider

from models.users import User
from models.posts import Post


class SQLiteDataProvider(XDataProvider):
    def __init__(self, filename, echo=False):
        if not filename or not filename.strip():
            raise ValueError("Необходимо указать имя файла базы данных.")

        conn_str = f'sqlite:///{filename.strip()}?check_same_thread=False'

        super().__init__(conn_str, echo)


class UserIdentity(XIdentityProvider):
    def register(self, user=None, **userdata):
        if user is None:
            if 'password' in userdata:
                userdata['password_hash'] = self.password_hash(userdata.pop('password'))
            user = User(**userdata)
        current_app.data_provider.add(user)

    def verify(self, user=None, **userdata):
        if user is None:
            user = self.find_user(**userdata)
        return user and self.check_password(user, userdata['password'])

    def find_user(self, **userdata):
        if 'email' in userdata:
            return User.query(User.email == userdata['email']).first()
        if 'username' in userdata:
            return User.query(User.username == userdata['username']).first()
        return None


class PitterApp(XApp):
    def setup_views(self):
        pass

    def setup_blueprints(self):
        from controllers.posts import PostsController
        PostsController.add_to_app(self, url_prefix='/')
        from controllers.auth import AuthController
        AuthController.add_to_app(self, url_prefix='/auth')
        from controllers.user import UserController
        UserController.add_to_app(self, url_prefix='/user')
        from controllers.error import ErrorController
        ErrorController.add_to_app(self, url_prefix='/error')

    def setup_data_providers(self):
        User.setup_table()
        Post.setup_table()

    def setup_identity_providers(self):
        self.identity_provider.user_loader(User.get)


def pitter():
    return PitterApp(config='application.cfg',
                    identity=UserIdentity,
                    data=XDataProvider)


if __name__ == '__main__':
    pitter().run()
