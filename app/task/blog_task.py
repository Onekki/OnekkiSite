import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from flask_mail import Message

from app.plugin import celery, mail
from app.database.models import BlogReminder

@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def remind(self, primary_key):
    reminder = BlogReminder.query.get(primary_key)
    
    msg = MIMEText(remind.content)
    msg['Subject'] = "Welcome!"
    msg['From'] = "<your email>"
    msg['To'] = reminder.email
    try:
        smtp_server = smtplib.SMTP('39.107.230.35')
        smtp_server.starttls()
        smtp_server.login("<user>", "<password>")
        smtp_server.sendmail(
            "<your_email>", [reminder.email], msg.as_string()
        )
        smtp_server.close()
        return
    except Exception as e:
        self.rety(exc=e)

def on_redminder_save(mapper, connect, self):
    remind.apply_async(args=(self.id), eta=self.date)

