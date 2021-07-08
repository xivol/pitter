from flask import url_for

from x_app.controller import XController
from controllers.params.user import USER_PARAM
from controllers.params.post import POST_PARAM
from view_models.user_feed import UserFeedViewModel
from view_models.user_post import UserPostViewModel, EditUserPostViewModel


class UserController(XController):
    def setup_endpoints(self):
        super().register_view_model(f'/{USER_PARAM}/post/{POST_PARAM}/edit',
                                    EditUserPostViewModel,
                                    'post-edit')
        super().register_view_model(f'/{USER_PARAM}/post/{POST_PARAM}/delete',
                                    UserPostViewModel,
                                    'post-delete')

        post_urls = {'post': lambda p: self.url_for('post', p),
                     'edit': lambda p: self.url_for('post-edit', p),
                     'delete': lambda p: self.url_for('post-delete', p),
                     'feed': lambda p: self.url_for('feed', p)}

        super().register_view_model(f'/{USER_PARAM}/post/{POST_PARAM}',
                                    UserPostViewModel,
                                    'post',
                                    model_config=post_urls)
        super().register_view_model(f'/{USER_PARAM}',
                                    UserFeedViewModel,
                                    'feed',
                                    model_config=post_urls)

    def url_for(self, endpoint, post):
        params = {USER_PARAM.name: post.user.username,
                  POST_PARAM.name: post.id}
        return url_for(f'{self.blueprint_name()}.{endpoint}', **params)
