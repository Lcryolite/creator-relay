"""Explicit, owner-configured SMTP delivery for a real Mind email address."""

from __future__ import annotations

import os
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage


@dataclass(frozen=True)
class SmtpConfig:
    host: str
    port: int
    username: str
    password: str
    sender: str

    @classmethod
    def from_environment(cls) -> "SmtpConfig":
        missing = [
            name
            for name in (
                "CREATOR_RELAY_SMTP_HOST",
                "CREATOR_RELAY_SMTP_USERNAME",
                "CREATOR_RELAY_SMTP_PASSWORD",
                "CREATOR_RELAY_SMTP_FROM",
            )
            if not os.getenv(name, "").strip()
        ]
        if missing:
            raise ValueError("missing SMTP configuration: " + ", ".join(missing))
        try:
            port = int(os.getenv("CREATOR_RELAY_SMTP_PORT", "465"))
        except ValueError as exc:
            raise ValueError("CREATOR_RELAY_SMTP_PORT must be an integer") from exc
        return cls(
            host=os.environ["CREATOR_RELAY_SMTP_HOST"],
            port=port,
            username=os.environ["CREATOR_RELAY_SMTP_USERNAME"],
            password=os.environ["CREATOR_RELAY_SMTP_PASSWORD"],
            sender=os.environ["CREATOR_RELAY_SMTP_FROM"],
        )


def send_smtp(message: EmailMessage, config: SmtpConfig) -> None:
    """Send one already-composed message; never called by the demo web UI."""
    message.replace_header("From", config.sender) if message["From"] else message.__setitem__("From", config.sender)
    with smtplib.SMTP_SSL(config.host, config.port, context=ssl.create_default_context()) as client:
        client.login(config.username, config.password)
        client.send_message(message)
