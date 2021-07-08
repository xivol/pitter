from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

from models.posts import Post, SHARE_OPTIONS


class NewTextPostForm(FlaskForm):
    author_id = HiddenField('Author',[DataRequired()])
    message = TextAreaField('Message', [DataRequired()])
    visibility = SelectField('Visibility', choices=SHARE_OPTIONS)
    submit = SubmitField('Share')

    def get_post(self):
        return Post(author_id=int(self.author_id.data),
                    content=self.message.data,
                    share_options=self.visibility.data)


class EditTextPostForm(FlaskForm):
    author_id = HiddenField('Author',[DataRequired()])
    post_id = HiddenField('Post', [DataRequired()])
    message = TextAreaField('Message', [DataRequired()])
    visibility = SelectField('Visibility', choices=SHARE_OPTIONS)
    confirm = SubmitField('Confirm')
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

    def set_post(self):
        return Post(author_id=int(self.author_id.data),
                    content=self.message.data,
                    share_options=self.visibility.data)


# from flask_wtf.file import FileField, FileAllowed, FileRequired
# from flask_uploads import UploadSet, IMAGES
# images = UploadSet('images', IMAGES)
# class NewImagePostForm(FlaskForm):
#     message = TextAreaField('Message', [DataRequired()])
#     image = FileField('Upload Image', [FileRequired(),
#                                        FileAllowed(images, 'Images only!')])
#     visibility = SelectField('Visibility', choices=SHARE_OPTIONS)
#     submit = SubmitField('Share')
