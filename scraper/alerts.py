import smtplib
import os
from email.message import EmailMessage
from typing import Optional

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")


def send_email(subject: str, body: str, to: Optional[str] = None) -> None:
    to = to or TO_EMAIL
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, FROM_EMAIL, to]):
        raise RuntimeError("SMTP configuration not set in environment")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
