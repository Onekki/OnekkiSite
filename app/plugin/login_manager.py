from flask_login import LoginManager
login_manager = LoginManager()

login_manager.login_view = "blog.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def user_loader(id):
    """Load the user's info."""

    from app.database.models import BlogUser
    return BlogUser.query.filter_by(id=id).first()