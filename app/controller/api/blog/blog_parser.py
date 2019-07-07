from flask_restful import reqparse


article_get_parser = reqparse.RequestParser()
article_get_parser.add_argument('page',
    type=int,
    location=['json', 'args', 'headers'],
    required=False)
article_get_parser.add_argument('user',
    type=str,
    location=['json', 'args', 'headers'])

article_post_parser = reqparse.RequestParser()
article_post_parser.add_argument('title',
    type=str,
    required=True,
    help="Title is required!")
article_post_parser.add_argument('content',
    type=str,
    required=True,
    help="Content is required!")
article_post_parser.add_argument('tags',
    type=str,
    action='append')
article_post_parser.add_argument('token',
    type=str,
    required=True,
    help="Auth Token is required to create article!")

userAuth_post_parser = reqparse.RequestParser()
userAuth_post_parser.add_argument('name',
    type=str,
    required=True,
    help="Name is required!")

userAuth_post_parser.add_argument('password',
    type=str,
    required=True,
    help="Password is required!")

article_put_parser = reqparse.RequestParser()
article_get_parser.add_argument('title',
    type=str)
article_get_parser.add_argument('content',
    type=str)
article_get_parser.add_argument('tags',
    type=str,
    action='append')
article_put_parser.add_argument('token',
    type=str,
    required=True,
    help="Auth Token is reqired to update the article!")

article_delete_parser = reqparse.RequestParser()
article_delete_parser.add_argument('token',
    type=str,
    required=True,
    help="Auth Token is reqired to update the article!")

