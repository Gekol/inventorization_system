import json
import os
import smtplib
import ssl

from django.contrib.auth.models import User
from core import Logger, _is_in_group

PORT = 465  # For SSL
SENDER_EMAIL = "sokolovsky17012001@gmail.com"
PASSWORD = os.environ["PASSWORD"]


class EmailSender:
    def __init__(self):
        self.logger = Logger()
        self.context = ssl.create_default_context()

    def send_email(self, message):
        emails = [user.email for user in User.objects.all() if _is_in_group(user, "admin")]
        print(emails)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=self.context) as server:
                server.login(SENDER_EMAIL, PASSWORD)
                for email in emails:
                    server.sendmail(SENDER_EMAIL, email, message)
        except Exception as exp:
            self.logger.emit_log("error", json.dumps({"error_message": str(exp)}))
