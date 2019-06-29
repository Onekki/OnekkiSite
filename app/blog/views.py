from flask import render_template, jsonify
from sqlalchemy import func
# from flask_sqlalchemy import Pagination
# 获取蓝图
from app.blog import blog
# 获取数据库模型对象和SQLAlchemy对象db，注意不可使用App模块中的db
# from app.blog.models import BlogArticle, BlogTag
# from app import db
from app.db.models import *

def json_return(code, msg,data):
    return jsonify({"code":code, "msg":msg, "data": data})

# 设置路由
@blog.route('/')
def index():
    return render_template("blog/index.html")
   
@blog.route("/article/<int:page>")
def article(page=1):
    articles = BlogArticle.query.paginate(page, 5)
    # return json_return(200, "success", [i.serialize for i in articles])
    return render_template("blog/article.html", articles=articles)

@blog.route("/user/<int:page>")
def user(page=1):
    users = BlogUser.query.all()
    # return json_return(200, "success", [i.serialize for i in articles])
    return render_template("blog/user.html", users=users)

@blog.route("/tag/<int:page>")
def tag(page=1):
    tags = BlogTag.query.all()
    # return json_return(200, "success", [i.serialize for i in articles])
    return render_template("blog/tag.html", tags=tags)

@blog.route("/comment/<int:page>")
def comment(page=1):
    comments = BlogComment.query.all()
    # return json_return(200, "success", [i.serialize for i in articles])
    return render_template("blog/comment.html", comments=comments)