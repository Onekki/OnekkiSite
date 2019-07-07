from flask_admin import BaseView, expose
from flask_login import login_required, current_user
from app.plugins import permission_admin

# 基础视图
class CustomView(BaseView):
    @expose('/')
    @login_required
    @permission_admin.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')
    
    @expose('/second_page')
    @login_required
    @permission_admin.require(http_exception=403)
    def second_page(self):
        return self.render('admin/second_page.html')

from flask_admin.contrib.sqla import ModelView
# 模型管理
class CustomModelView(ModelView):

    def is_accessible(self):
        user = current_user
        return current_user.is_authenticated() and permission_admin.can()

from app.forms.blog import CKTextAreaField
# 文章修改增强
class ArticleView(CustomModelView):
    form_overrides = dict(content=CKTextAreaField)

    column_searchable_list = ('content', 'title')

    column_filters = ('publish_time',)

    create_template = 'admin/article_update.html'

    edit_template = 'admin/article_update.html'

from flask_admin.contrib.fileadmin import FileAdmin
# 文件管理
class CustomFileView(FileAdmin):
    def is_accessible(self):
       return current_user.is_authenticated() and permission_admin.can()

