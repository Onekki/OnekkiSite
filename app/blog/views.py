import datetime
from flask import render_template, jsonify, request
from sqlalchemy import func
# from flask_sqlalchemy import Pagination
# 获取蓝图
from app.blog import blog
# 获取数据库模型对象和SQLAlchemy对象db，注意不可使用App模块中的db
# from app.blog.models import BlogArticle, BlogTag
# from app import db
from app.db.models import *
# 导入表单验证
from app.form.forms import CommentForm

def json_return(code, msg,data):
    return jsonify({'code':code, 'msg':msg, 'data': data})

def sidebar_data():
    recent_article_list = BlogArticle.query.order_by(
        BlogArticle.publish_time.desc()
    ).limit(5).all()
    count = func.count(BlogArticle.id).label('total')
    top_tag_list = db.session.query(
        BlogTag.id, BlogTag.name, count
    ).filter(
        BlogArticle.tag_id==BlogTag.id
    ).group_by(BlogTag.id).order_by(count.desc()).limit(5).all()

    return recent_article_list, top_tag_list

# 设置路由
@blog.route('/')
def index():
    return render_template('blog/index.html', data = sidebar_data())

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
    tag_list = [article.tag]
    comment_list = BlogComment.query.filter(BlogComment.article_id==id).all()
    
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
        filters.append(BlogArticle.tag_id==tag_id)
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