from flask_wtf import FlaskForm
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    name = StringField(
        '评论人',
        validators=[DataRequired(), Length(max=255)]
    )
    content = TextField(
        '评论内容',
        validators = [DataRequired()]
    )   