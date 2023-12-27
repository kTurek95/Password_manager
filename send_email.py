import smtplib
from os import getenv
from email.mime.text import MIMEText
from dotenv import load_dotenv


class Email:
    load_dotenv()

    def __init__(self, receiver_email, receiver_name):
        self.receiver_email = receiver_email
        self.receiver_name = receiver_name

    @staticmethod
    def smtp_settings():
        smtp_server = getenv('SMTP_SERVER')
        smtp_port = int(getenv('SMTP_PORT'))
        smtp_username = getenv('MAIL_USERNAME')
        smtp_password = getenv('MAIL_PASSWORD')
        sender = getenv('SENDER')

        return smtp_server, smtp_port, smtp_username, smtp_password, sender

    def send_mail(self):
        subject = 'Password Manager'
        message = f'Hello {self.receiver_name} your account is now registered'
        smtp_server, smtp_port, smtp_username, smtp_password, sender = self.smtp_settings()

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = self.receiver_email


        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, self.receiver_email, msg.as_string())
