import datetime
from flask import render_template, redirect, jsonify, request, flash, url_for, get_flashed_messages
from sqlalchemy import func
# from flask_sqlalchemy import Pagination

from app import db
# 获取蓝图
from app.blog import blog
# 获取数据库模型对象和SQLAlchemy对象db，注意不可使用App模块中的db
# from app.blog.models import BlogArticle, BlogTag
# from app import db
from app.database.models import *
# 导入表单验证
from app.form.forms import *

def json_return(code, msg,data):
    return jsonify({'code':code, 'msg':msg, 'data': data})

def sidebar_data():
    recent_article_list = BlogArticle.query.order_by(
        BlogArticle.publish_time.desc()
    ).limit(5).all()
    count = func.count(t_blog_article_tag.c.article_id).label('total')

    top_tag_list = db.session.query(
        BlogTag.id, BlogTag.name, count
    ).filter(
        BlogTag.id==t_blog_article_tag.c.tag_id
    ).group_by(BlogTag.id).order_by(count.desc()).limit(5).all()

    return recent_article_list, top_tag_list

# 设置路由
@blog.route('/')
def index():
    return render_template('blog/index.html', data = sidebar_data())
# 注册
@blog.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = BlogUser(name=form.name.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("注册成功, 请登录!")
        
        return redirect(url_for('blog.login'))
    return render_template('blog/register.html',form=form)

# 登录
@blog.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("登录成功", category="success")
        return redirect(url_for('blog.article_list', page=1))
    return render_template('blog/login.html',form=form)
# 登出
@blog.route('/logout', methods=['GET', 'POST'])
def logout():
    flash("退出登录成功", category="success")
    return redirect(url_for('blog.article_list'))

# 新增文章
@blog.route('/article_add', methods=['GET', 'POST'])
def article_add():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = BlogArticle()
        new_article.title = form.title.data
        new_article.content = form.content.data
        new_article.publish_time = datetime.datetime.now()

        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('blog.article_list', page=1))

    return render_template('blog/article_add.html', form=form)

# 修改文章
@blog.route('/article_update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = BlogArticle.query.get_or_404(id)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.publish_time = datetime.datetime.now()

        db.session.add(article)
        db.session.commit()
        return redirect(url_for('blog.article', id=article.id))
    
    form.title.data = article.title
    form.content.data = article.content
    return render_template('blog/article_update.html', form=form, article=article)

# 获取文章
@blog.route('/article/<int:id>', methods=['GET','POST'])
def article(id):

    form = CommentForm()
    if form.validate_on_submit():
        new_comment = BlogComment()
        new_comment.name=form.name.data
        new_comment.content=form.content.data
        new_comment.time=datetime.datetime.now()
        new_comment.article_id=id
        db.session.add(new_comment)
        db.session.commit()

    article = BlogArticle.query.get_or_404(id)
    tag_list = article.tags
    comment_list = article.comments.order_by(BlogComment.time.desc()).all()
    
    recent_article_list, top_tag_list = sidebar_data()

    return render_template('blog/article.html',
                            article=article,
                            form=form,
                            tag_list=tag_list,
                            comment_list=comment_list,
                            recent_article_list=recent_article_list,
                            top_tag_list=top_tag_list)

@blog.route('/article_list/<int:page>')
def article_list(page):
    filters = []
    tag_id = request.values.get('tag_id')
    if tag_id != None:
        print(tag_id)
        filters.append(t_blog_article_tag.c.tag_id==tag_id)
        filters.append(t_blog_article_tag.c.article_id==BlogArticle.id)
    article_list = BlogArticle.query.filter(*filters).paginate(page, 5)

    recent_article_list, top_tag_list = sidebar_data()
    # return json_return(200, 'success', [i.serialize for i in articles])
    return render_template('blog/article_list.html', 
                            tag_id=tag_id,
                            article_list=article_list, 
                            recent_article_list=recent_article_list,
                            top_tag_list=top_tag_list)

@blog.route('/user_list/<int:page>')
def user_list(page):
    users = BlogUser.query.all()
    # return json_return(200, 'success', [i.serialize for i in articles])
    return render_template('blog/user.html', users=users)

@blog.route('/tag_list/<int:page>')
def tag_list(page):
    tags = BlogTag.query.all()
    # return json_return(200, 'success', [i.serialize for i in articles])
    return render_template('blog/tag.html', tags=tags)

@blog.route('/comment_list/<int:page>')
def comment_list(page):
    comments = BlogComment.query.all()
    # return json_return(200, 'success', [i.serialize for i in articles])
    return render_template('blog/comment.html', comments=comments)