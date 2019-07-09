# 系统模块
import datetime
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
from sqlalchemy import func
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
# 插件
from app.controller.blog import blog
from app.plugins import (
    db, 
    permission_poster, 
    permission_admin, 
    cache
)
from app.database.models import *
# 导入表单验证
from app.forms.blog import *

# 侧边栏
@cache.cached(timeout=7200, key_prefix='sidebar_dada')
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


# 新增文章
@blog.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = BlogArticle()
        new_article.title = form.title.data
        new_article.content = form.content.data
        new_article.publish_time = datetime.datetime.now()
        new_article.user = current_user

        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('blog.article_list', page=1))

    return render_template('blog/article/add.html', obj_form=form)

# 修改文章
@blog.route('/article/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_poster.require(http_exception=403)
def article_edit(id):
    article = BlogArticle.query.get_or_404(id)

    if not current_user:
        return redirect(url_for('site.login'))

    if current_user != article.user:
        return redirect(url_for('blog.article_one', id=id))
    
    permission = Permission(UserNeed(article.user.id))
    if permission.can() or permission_admin.can():
        form = ArticleForm()
        if form.validate_on_submit():
            article.title = form.title.data
            article.content = form.content.data
            article.publish_time = datetime.datetime.now()

            db.session.add(article)
            db.session.commit()
            return redirect(url_for('blog.article_one', id=article.id))
    else:
        abort(403)
    
    form.title.data = article.title
    form.content.data = article.content
    return render_template('blog/article/edit.html', obj_form=form, article_one=article)

# 缓存的key
def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')

# 获取文章
@blog.route('/article/one/<int:id>', methods=['GET','POST'])
# @cache.cached(timeout=60, key_prefix=make_cache_key)
def article_one(id):

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

    return render_template('blog/article/one.html',
                            article_one=article,
                            obj_form=form,
                            tag_list=tag_list,
                            comment_list=comment_list,
                            recent_article_list=recent_article_list,
                            top_tag_list=top_tag_list)

# 文章列表
@blog.route('/article/list/<int:page>')
# @cache.cached(timeout=60)
def article_list(page):
    filters = []
    tag_id = request.values.get('tag_id')
    if tag_id != None:
        filters.append(t_blog_article_tag.c.tag_id==tag_id)
        filters.append(t_blog_article_tag.c.article_id==BlogArticle.id)
    article_list = BlogArticle.query.filter(*filters).paginate(page, 8)

    recent_article_list, top_tag_list = sidebar_data()
    # return json_return(200, 'success', [i.serialize for i in articles])
    return render_template('blog/article/list.html', 
                            tag_id=tag_id,
                            article_list=article_list, 
                            recent_article_list=recent_article_list,
                            top_tag_list=top_tag_list)
