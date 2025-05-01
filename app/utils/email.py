import os
import smtplib
from email.message import EmailMessage

def send_email(to, subject, body, is_html=False):
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Missing email credentials in environment variables.")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to

    if is_html:
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)

    with smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
