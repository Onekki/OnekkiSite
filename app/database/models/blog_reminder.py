from app.plugins import db

class BlogReminder(db.Model):
    __tablename__ = 'blog_reminder'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    email = db.Column(db.String(255))
    content = db.Column(db.Text)