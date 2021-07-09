from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

from models.posts import Post, SHARE_OPTIONS


class NewTextPostForm(FlaskForm):
    author_id = HiddenField('Author', [DataRequired()])
    message = TextAreaField('Message', [DataRequired()])
    visibility = SelectField('Visibility', choices=SHARE_OPTIONS)
    submit = SubmitField('Share')

    def get_post(self):
        return Post(author_id=int(self.author_id.data),
                    content=self.message.data,
                    share_options=self.visibility.data)


class BasicTextPostForm(FlaskForm):
    author_id = HiddenField('Author', [DataRequired()])
    post_id = HiddenField('Post', [DataRequired()])
    confirm = SubmitField('Confirm')
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

    def set_post(self, post):
        self.author_id.data = post.user_id
        self.post_id.data = post.id


class EditTextPostForm(BasicTextPostForm):
    message = TextAreaField('Message', [DataRequired()])
    visibility = SelectField('Visibility', choices=SHARE_OPTIONS)

    def __init__(self):
        super().__init__()
        self.title = 'Edit your publication'

    def set_post(self, post):
        super().set_post(post)
        self.message.data = post.content
        self.visibility.data = SHARE_OPTIONS[post.share_options]


class DeleteTextPostForm(BasicTextPostForm):
    def __init__(self):
        super().__init__()
        self.title = 'Delete your publication'
        self.message = ''

# from flask_wtf.file import FileField, FileAllowed, FileRequired
# from flask_uploads import UploadSet, IMAGES
# images = UploadSet('images', IMAGES)
# class NewImagePostForm(FlaskForm):
#     message = TextAreaField('Message', [DataRequired()])
#     image = FileField('Upload Image', [FileRequired(),
#                                        FileAllowed(images, 'Images only!')])
#     visibility = SelectField('Visibility', choices=SHARE_OPTIONS)
#     submit = SubmitField('Share')
