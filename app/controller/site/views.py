from flask import (
    render_template, 
    redirect, 
    jsonify, 
    request, 
    flash, 
    url_for, 
    get_flashed_messages, 
    abort
)
from flask_login import (
    login_user, 
    logout_user, 
    login_required, 
    current_user
)
from flask_principal import (
    identity_changed, 
    current_app, 
    Identity,
    AnonymousIdentity, 
    Permission, 
    UserNeed
)
from app.plugins import (
    db, 
    permission_poster, 
    permission_admin, 
    cache
)
from app.database.models import BlogUser
# 导入表单验证
from app.forms.auth import *


# 获取蓝图
from app.controller.site import site

# 设置路由
@site.route('/')
def index():
    return render_template('site/index.html')

# 注册
@site.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = BlogUser(name=form.name.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("注册成功, 请登录!")
        
        return redirect(url_for('site.login'))
    return render_template('auth/register.html',obj_form=form)

# 登录
@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = BlogUser.query.filter_by(name=form.name.data).one()

        login_user(user, remember=form.remember.data)
        identity_changed.send(
            current_app._get_current_object(), identity=Identity(user.id)
        )

        flash("登录成功", category="success")
        return redirect(url_for('blog.article_list', page=1))
    return render_template('auth/login.html',obj_form=form)

# 登出
@site.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity()
    )
    flash("退出登录成功", category="success")
    return redirect(url_for('site.login'))
