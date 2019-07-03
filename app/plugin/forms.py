from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, IntegerField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

from app.database.models import BlogUser

class RegisterForm(FlaskForm):
    name = StringField('name', [DataRequired(), Length(max=255)])
    password = PasswordField('password', [DataRequired(), Length(min=2)])
    confirm = PasswordField('password', [DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    
    def validate(self):
        is_valid = super(RegisterForm, self).validate()

        # 输入是否合法
        if not is_valid:
            return False
        
        # 用户是否存在
        user = BlogUser.query.filter_by(name=self.name.data).first()
        if user:
            self.name.errors.append('用户已经存在')
            return False
        return True

class LoginForm(FlaskForm):
    name = StringField('name', [DataRequired(), Length(max=255)])
    password = PasswordField('password', [DataRequired()])
    remember = BooleanField('remember')
    def validate(self):
        is_valid = super(LoginForm, self).validate()
        
        # 输入是否合法
        if not is_valid:
            return False
        # 用户是否存在
        user = BlogUser.query.filter_by(name=self.name.data).first()
        if not user:
            self.name.errors.append('用户不存在')
            return False
        # 密码是否正确
        if not user.check_password(self.password.data):
            self.name.errors.append("密码错误")
            return False
        return True
    
class ArticleForm(FlaskForm):
    title = StringField('title', [DataRequired(), Length(max=255)])
    content = TextAreaField('content', [DataRequired()])

class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    content = TextField(
        'Content',
        validators = [DataRequired()]
    )