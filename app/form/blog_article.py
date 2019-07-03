from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class ArticleForm(FlaskForm):
    title = StringField('title', [DataRequired(), Length(max=255)])
    content = TextAreaField('content', [DataRequired()])