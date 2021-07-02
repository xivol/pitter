from flask import current_app

from x_app.app import XApp
from x_app.data_provider import SQLiteDataProvider
from x_app.identity_provider import XIdentityProvider

from models.users import User
from models.news import News



class UserIdentity(XIdentityProvider):
    def register(self, **userdata):
        if 'password' in userdata:
            userdata['password_hash'] = self.password_hash(userdata.pop('password'))
        user = User(**userdata)
        User.add(user)

    def verify(self, **userdata):
        user = User.query(User.email == userdata['email']).first()
        return user and self.check_password(user, userdata['password'])


class FirstApp(XApp):
    def setup_views(self):
        pass

    def setup_blueprints(self):
        from controllers.news import NewsController
        NewsController.add_to_app(self, url_prefix='/')
        from controllers.users import UserController
        UserController.add_to_app(self, url_prefix='/user')

    def setup_data_providers(self):
        current_app.data_provider = SQLiteDataProvider("../flask_mvp/static/data/blogs.sqlite")
        User.setup_table()
        News.setup_table()

    def setup_identity_providers(self):
        current_app.identity_provider.user_loader(User.get)


if __name__ == '__main__':
    app = FirstApp(config='application.cfg', identity=UserIdentity())
    app.start()