from controllers.params.route_param import RouteParam
from models.posts import Post

POST_PARAM = RouteParam('int', 'post_id', 'id')


def get_post(view_model, on_post_found, on_post_not_found, on_param_error):
    if view_model[POST_PARAM.name]:
        p = Post.query(getattr(Post, POST_PARAM.model) == view_model[POST_PARAM.name]).first()
        if p is not None:
            return on_post_found(p)
        else:
            return on_post_not_found(POST_PARAM, view_model[POST_PARAM.name])
    on_param_error(POST_PARAM)
