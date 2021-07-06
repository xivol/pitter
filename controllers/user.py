from flask import request, redirect, current_app, abort
from flask_login import current_user

from models.posts import Post
from view_models.user import UserFeedViewModel, USERNAME_PARAM
from x_app.controller import XController


class UserController(XController):
    def setup_endpoints(self):
        super().register_view_model(f'/<string:{USERNAME_PARAM}>',
                                    UserFeedViewModel,
                                    'feed')
