from abc import ABC, abstractmethod

from flask import request, flash, url_for, redirect, current_app
from flask_sqlalchemy_session import current_session
from werkzeug.exceptions import abort

from view_models.forms.post import EditTextPostForm, DeleteTextPostForm
from view_models.mixins.navigation import NavigationViewModel
from controllers.params.user import USER_PARAM, get_user
from controllers.params.post import POST_PARAM, get_post
from x_app.view_model import XPageModel, XFormPage


class UserPostViewModel(XPageModel, NavigationViewModel):
    __request_params__ = {USER_PARAM.name, POST_PARAM.name}
    __template_name__ = 'post.html'

    def __init__(self, **url_providers):
        super().__init__('Post')
        self.user = None
        self.post = None
        self.urls = url_providers

    def on_request(self, request):
        self.user = None
        return get_user(self, self.on_user_found,
                        on_user_not_found=lambda k, v: abort(404),
                        on_param_error=lambda x: abort(400))

    def on_user_found(self, user):
        self.user = user
        self.post = None
        return get_post(self, self.on_post_found,
                        on_post_not_found=lambda k, v: abort(404),
                        on_param_error=lambda x: abort(400))

    def on_post_found(self, post):
        if post.user != self.user:
            abort(404)

        self.post = post
        self.title = f'@{self.user.username} on {self.post.created_date}'
        return super().render_template()


class BasicPostFormViewModel(XFormPage, NavigationViewModel):
    __request_params__ = {USER_PARAM.name, POST_PARAM.name}

    def on_form_error(self, form):
        flash(form.errors, 'danger')
        return super().render_template()

    def make_form(self):
        return get_user(self, self.on_user_found,
                        on_user_not_found=lambda k, v: abort(404),
                        on_param_error=lambda x: abort(400))

    def on_user_found(self, user):
        self.user = user
        if not user.is_authenticated:
            abort(401)

        return get_post(self, self.on_post_found,
                        on_post_not_found=lambda x, v: abort(404),
                        on_param_error=lambda x: abort(400))

    @abstractmethod
    def on_post_found(self, post):
        pass


class EditUserPostViewModel(BasicPostFormViewModel):
    __template_name__ = 'post.html'

    def __init__(self):
        super().__init__('Post Edit')

    def on_form_success(self, form):
        if form.confirm.data:
            self.post.update(form.message.data, form.visibility.data)
            current_session.commit()
            flash('Post has been edited!', 'success')

        params = {USER_PARAM.name: self.user.username,
                  POST_PARAM.name: self.post.id}
        return redirect(url_for('user.post', **params))

    def on_post_found(self, post):
        if post.user != self.user:
            abort(404)

        self.post = post
        self.title = f'Edit message posted on {self.post.created_date}'

        form = EditTextPostForm()
        if request.method == 'GET':
            form.set_post(post)
        return form


class DeleteUserPostViewModel(BasicPostFormViewModel):
    __template_name__ = 'post.html'

    def __init__(self):
        super().__init__('Post Delete')

    def on_form_success(self, form):
        if form.confirm.data:
            current_session.delete(self.post)
            current_session.commit()
            flash('Yor post has been deleted!', 'success')

        params = {USER_PARAM.name: self.user.username}
        return redirect(url_for('user.feed', **params))

    def on_post_found(self, post):
        if post.user != self.user:
            abort(404)

        self.post = post
        self.title = f'Delete message posted on {self.post.created_date}'

        form = DeleteTextPostForm()
        form.title = "Are you sure?"
        form.message = "You are about to delete this message. This action is irreversible."

        if request.method == 'GET':
            form.set_post(post)
        return form
