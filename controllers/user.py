from flask import url_for, current_app
from flask_login import login_required

from x_app.controller import XController
from controllers.params.user import USER_PARAM
from controllers.params.post import POST_PARAM
from view_models.user_feed import UserFeedViewModel
from view_models.user_post import UserPostViewModel, EditUserPostViewModel, DeleteUserPostViewModel


class UserController(XController):
    def setup_endpoints(self):
        super().register_view_model(f'/{USER_PARAM}/post/{POST_PARAM}/edit',
                                    EditUserPostViewModel,
                                    'post-edit',
                                    login_required=True)
        super().register_view_model(f'/{USER_PARAM}/post/{POST_PARAM}/delete',
                                    DeleteUserPostViewModel,
                                    'post-delete',
                                    login_required=True)

        super().register_view_model(f'/{USER_PARAM}/post/{POST_PARAM}',
                                    UserPostViewModel,
                                    'post',
                                    model_config=self.get_url_providers())
        super().register_view_model(f'/{USER_PARAM}',
                                    UserFeedViewModel,
                                    'feed',
                                    model_config=self.get_url_providers())

    @classmethod
    def url_for(cls, endpoint, post):
        params = {USER_PARAM.name: post.user.username}
        if 'post' in endpoint:
            params[POST_PARAM.name] = post.id
        return url_for(f'{cls.blueprint_name()}.{endpoint}', **params)

    @staticmethod
    def get_url_providers():
        return {'post': lambda p: UserController.url_for('post', p),
                'edit': lambda p: UserController.url_for('post-edit', p),
                'delete': lambda p: UserController.url_for('post-delete', p),
                'feed': lambda p: UserController.url_for('feed', p)}
