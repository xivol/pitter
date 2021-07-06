from flask import request, redirect, current_app, abort
from flask_login import current_user

from models.posts import Post
from view_models.forms.post import NewTextPostForm
from view_models.timeline import IndexViewModel
from x_app.controller import XController


class PostsController(XController):
    def setup_endpoints(self):
        super().register_view_model('/', IndexViewModel, 'latest')
        super().register_view_func('/post/new', self.new_post, 'new', methods=['POST'])
        super().register_view_func('/post/<int:post_id>', self.get_post, 'single')
        super().register_view_func('/post/delete/<int:post_id>', self.get_post, 'delete')
        super().register_view_func('/post/update/<int:post_id>', self.get_post, 'update')

    def new_post(self):
        print(request.form)
        form = NewTextPostForm()
        if form.validate_on_submit():
            if current_user.is_authenticated and \
                    current_user.id == (int(form.author_id.data)):
                current_app.data_provider.add(form.get_post())
            else:
                return abort(403)
        return redirect(request.referrer)

    def get_post(self, post_id):
        raise NotImplementedError()
