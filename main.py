from flask import current_app

from x_app.app import XApp
from x_app.data_provider import SQLiteDataProvider
from x_app.identity_provider import XIdentityProvider

from models.users import User
from models.posts import Post


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
        return User.query(User.email == userdata['email']).first()


class FirstApp(XApp):
    def setup_views(self):
        pass

    def setup_blueprints(self):
        from controllers.posts import PostsController
        PostsController.add_to_app(self, url_prefix='/')
        from controllers.auth import AuthController
        AuthController.add_to_app(self, url_prefix='/auth')
        from controllers.user import UserController
        UserController.add_to_app(self, url_prefix='/user')

    def setup_data_providers(self):
        current_app.data_provider = SQLiteDataProvider("../pitter/data/blogs.sqlite")
        User.setup_table()
        Post.setup_table()

    def setup_identity_providers(self):
        current_app.identity_provider.user_loader(User.get)


if __name__ == '__main__':
    app = FirstApp(config='application.cfg', identity=UserIdentity())
    app.start()
