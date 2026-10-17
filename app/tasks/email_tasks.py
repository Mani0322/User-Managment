import smtplib
from email.message import EmailMessage

from app.tasks.celery_app import celery_app
from app.core.config import settings

@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def send_welcome_email(self, email: str, full_name: str | None):
    msg = EmailMessage()
    msg["Subject"] = "Welcome!"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email
    msg.set_content(f"Hi {full_name or 'there'},\n\nYour account has been created.")

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USER:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as exc:
        raise self.retry(exc=exc)