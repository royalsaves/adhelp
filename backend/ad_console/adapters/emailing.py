from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3

from ad_console.config import Settings
from ad_console.domain.models import EmailMessage


class ConsoleEmailAdapter:
    def send(self, message: EmailMessage) -> None:
        print(f"[demo] email to={message.to} subject={message.subject}")


class SmtpEmailAdapter:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def send(self, message: EmailMessage) -> None:
        payload = MIMEMultipart("alternative")
        payload["From"] = self._settings.from_email
        payload["To"] = message.to
        payload["Subject"] = message.subject
        payload.attach(MIMEText(message.html, "html", "utf-8"))

        server = smtplib.SMTP(self._settings.smtp_host, self._settings.smtp_port)
        server.starttls()
        if self._settings.smtp_user and self._settings.smtp_password:
            server.login(self._settings.smtp_user, self._settings.smtp_password)
        server.send_message(payload)
        server.quit()


class SesEmailAdapter:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = boto3.client("ses", region_name=settings.aws_region)

    def send(self, message: EmailMessage) -> None:
        self._client.send_email(
            Source=self._settings.from_email,
            Destination={"ToAddresses": [message.to]},
            Message={
                "Subject": {"Data": message.subject, "Charset": "UTF-8"},
                "Body": {"Html": {"Data": message.html, "Charset": "UTF-8"}},
            },
        )
