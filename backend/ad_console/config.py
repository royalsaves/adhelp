from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_mode: str = os.getenv("APP_MODE", "demo").lower()
    service_name: str = os.getenv("SERVICE_NAME", "Identity Access Support Console")
    service_domain: str = os.getenv("SERVICE_DOMAIN", "localhost:5001")
    company_name: str = os.getenv("COMPANY_NAME", "ExampleCorp")
    company_domain: str = os.getenv("COMPANY_DOMAIN", "example.com")
    support_email: str = os.getenv("SUPPORT_EMAIL", "support@example.com")

    aws_region: str = os.getenv("AWS_REGION", "ap-northeast-2")
    directory_id: str | None = os.getenv("DIRECTORY_ID")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-this-secret")

    slack_webhook_url: str | None = os.getenv("SLACK_WEBHOOK_URL")
    ansible_api_url: str = os.getenv(
        "ANSIBLE_API_URL", "https://automation.example.com/api/jobs/account-unlock"
    )
    ansible_token: str | None = os.getenv("ANSIBLE_TOKEN")

    smtp_host: str = os.getenv("SMTP_HOST", "localhost")
    smtp_port: int = int(os.getenv("SMTP_PORT", "1025"))
    smtp_user: str | None = os.getenv("SMTP_USER")
    smtp_password: str | None = os.getenv("SMTP_PASSWORD")
    from_email: str = os.getenv("FROM_EMAIL", "noreply@example.com")

    ldap_host: str = os.getenv("LDAP_HOST", "ldap.example.internal")
    bedrock_model_id: str = os.getenv(
        "BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-20250514-v1:0"
    )

    @classmethod
    def is_demo(cls) -> bool:
        return cls().app_mode == "demo"
