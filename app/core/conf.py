# from . import login_manager

# # 登录页面的视图函数
# login_manager.login_view = "blog.login"
# # 能够更好的防止恶意用户篡改 cookies, 当发现 cookies 被篡改时, 该用户的 session 对象会被立即删除, 导致强制重新登录. 
# login_manager.session_protection = "strong"
# # 指定了提供用户登录的方案
# login_manager.login_message = "Please login to access this page."
# # 指定了登录信息的类别为 info 
# login_manager.login_message_category = "info"

# # 回调函数
# # 在用户登录并调用 login_user() 的时候, 根据 user_id 找到对应的 user, 如果没有找到，返回None, 此时的 user_id 将会自动从 session 中移除, 若能找到 user ，则 user_id 会被继续保存.
# @login_manager.user_loader
# def user_loader(id):
#     from app.db.models import BlogUser
#     return BlogUser.query.filter_by(id=id).first()
