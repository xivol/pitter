from controllers.params.route_param import RouteParam
from models.users import User

USER_PARAM = RouteParam('string', 'username')


def get_user(view_model, on_user_found, on_user_not_found, on_param_error):
    if view_model[USER_PARAM.name]:
        u = User.query(getattr(User, USER_PARAM.model) == view_model[USER_PARAM.name]).first()
        if u is not None:
            return on_user_found(u)
        else:
            return on_user_not_found(USER_PARAM, view_model[USER_PARAM.name])
    on_param_error(USER_PARAM)
