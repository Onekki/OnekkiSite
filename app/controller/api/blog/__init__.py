import datetime
from flask import jsonify, abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_principal import current_app
from flask_restful import Resource, marshal_with
from app.database.models import *
from app.plugins import db

from .blog_parser import *
from .blog_fields import result_fields

# 认证api
class BlogAuthApi(Resource):
    def post(self):
        args = userAuth_post_parser.parse_args()
        user = BlogUser.query.filter_by(name=args['name']).first()
        if user.check_password(args['password']):
            serializer = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=600
            )
            return {"token": serializer.dumps({"id":user.id}).decode('utf-8')}
        else:
            abort(401)

# 文章api
class BlogArticleApi(Resource):

# 获取文章
    @marshal_with(result_fields)
    def get(self, id=None):
        if id:
            article = BlogArticle.query.filter_by(id=id).first()
            if not article:
                abort(404)
            return {"data": article}
        else:
            args = article_get_parser.parse_args()
            page = args['page'] or 1
            
            if args['user']:
                user = BlogUser.query.filter_by(name=args['user']).first()
                if not user:
                    abort(404)
                article_list = user.articles.order_by(
                    BlogArticle.publish_time.desc()
                ).paginate(page, 10)
            else:
                article_list = BlogArticle.query.order_by(
                    BlogArticle.publish_time.desc()
                ).paginate(page, 10)
            
            return {"data": article_list.items}
    
# 创建文章
    def post(self, id=None):
        if id:
            abort(400)
        else:
            args = article_post_parser.parse_args(strict=True)

            user = BlogUser.verify_auth_token(args['token'])
            if not user:
                abort(401)

            new_article = BlogArticle()
            new_article.title = args['title']
            new_article.content = args['content']
            new_article.publish_time = datetime.datetime.now()
            new_article.user = user

            if args['tags']:
                for item in args['tags']:
                    tag = BlogTag.query.filter_by(name=item).first()
                    if tag:
                        new_article.tags.append(tag)
                    else:
                        new_tag = BlogTag()
                        new_tag.name = item
                        new_article.tags.append(new_tag)
        db.session.add(new_article)
        db.session.commit()
        return (new_article.id, 201)

# 修改文章
    def put(self, id=None):
        if not id:
            abort(400)

        article = BlogArticle.query.filter_by(id=id).first()
        if not article:
            abort(404)

        args = article_put_parser.parse_args()
        user = BlogUser.verify_auth_token(args['token'])

        if not user:
            abort(401)
        if user != article.user:
            abort(403)
    
        if args['title']:
            article.title = args['title']
        if args['content']:
            article.content = args['content']
        if args['tags']:
            for item in args['tags']:
                tag = BlogTag.query.filter_by(name=item).first()
                if tag:
                    article.tags.append(tag)
                else:
                    new_tag = BlogTag()
                    new_tag.name = item
                    article.tags.append(new_tag)
        db.session.add(article)
        db.session.commit()

        return (article.id, 201)

# 删除文章
    def delete(self, id=None):
        if not id:
            abort(400)
        
        article = BlogArticle.query.filter_by(id=id).first()
        if not article:
            abort(401)
        
        args = article_delete_parser.parse_args(strict=True)
        user = BlogUser.verify_auth_token(args['token'])
        if user != article.user:
            abort(403)
        
        db.session.delete(article)
        db.session.commit()

        return "", 204
