import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_FROM = os.getenv('MAIL_FROM')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_TLS = os.getenv('MAIL_TLS', 'True') == 'True'
MAIL_SSL = os.getenv('MAIL_SSL', 'False') == 'True'

def send_verification_email(to_email: str, verify_url: str):
    subject = "Verify your email"
    body = f"Click the link to verify your email: {verify_url}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = to_email

    if MAIL_SSL:
        server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    else:
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        if MAIL_TLS:
            server.starttls()
    server.login(MAIL_USERNAME, MAIL_PASSWORD)
    server.sendmail(MAIL_FROM, [to_email], msg.as_string())
    server.quit() 