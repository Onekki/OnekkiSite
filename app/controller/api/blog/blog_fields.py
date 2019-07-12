from flask_restful import fields

nested_tag_fields = {
    'id': fields.String(),
    'name': fields.String()
}

article_fields = {
    'author': fields.String(attribute=lambda x: x.user.name),
    'title': fields.String(),
    'content': fields.String(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_time': fields.DateTime(dt_format='iso8601')
}


result_fields = {
    'data': fields.List(fields.Nested(article_fields))
}