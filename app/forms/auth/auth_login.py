from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

from app.database.models import BlogUser

class LoginForm(FlaskForm):
    name = StringField('用户名', [DataRequired(), Length(max=255)])
    password = PasswordField('密码', [DataRequired()])
    remember = BooleanField('记住密码')
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
    