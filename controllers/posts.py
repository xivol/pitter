from flask import request, redirect, current_app, abort
from flask_login import current_user

from controllers.user import UserController
from view_models.forms.post import NewTextPostForm
from view_models.index import IndexViewModel
from x_app.controller import XController


class PostsController(XController):
    def setup_endpoints(self):
        super().register_view_model('/',
                                    IndexViewModel,
                                    'latest',
                                    model_config=UserController.get_url_providers())
        super().register_view_func('/post/new',
                                   self.new_post,
                                   'new',
                                   methods=['POST'])

    def new_post(self):
        form = NewTextPostForm()
        if form.validate_on_submit():
            if current_user.is_authenticated and \
                    current_user.id == (int(form.author_id.data)):
                current_app.data_provider.add(form.get_post())
            else:
                abort(401)
        return redirect(request.referrer)
