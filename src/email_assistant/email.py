import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("SENDER_EMAIL_ADDRESS")
PASSWORD = os.getenv("APP_PASSWORD")   # Use Gmail App Password

def send_email(email_content: str, email_address: str, email_subject: str):
    """Send an email via Gmail SMTP."""

    if not SENDER or not PASSWORD:
        raise ValueError("Email credentials are missing in .env")

    msg = EmailMessage()
    msg["Subject"] = email_subject
    msg["From"] = SENDER
    msg["To"] = email_address
    msg.set_content(email_content)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SENDER, PASSWORD)
            server.send_message(msg)

        return True

    except smtplib.SMTPAuthenticationError:
        raise Exception("Gmail authentication failed. Check your App Password.")

    except Exception as e:
        raise Exception(f"Failed to send email: {e}")