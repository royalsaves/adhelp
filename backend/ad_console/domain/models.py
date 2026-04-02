from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AccountRequest:
    request_id: str
    username: str
    email: str
    full_name: str
    department: str
    reason: str
    created_at: datetime


@dataclass
class UnlockRequest:
    request_id: str
    username: str
    email: str
    reason: str
    created_at: datetime


@dataclass
class VerificationCode:
    username: str
    email: str
    code: str
    expires_at: datetime


@dataclass
class EmailMessage:
    to: str
    subject: str
    html: str


@dataclass
class ChatMessage:
    role: str
    text: str


@dataclass
class DirectoryUser:
    username: str
    email: str
    full_name: str


@dataclass
class OperationResult:
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
