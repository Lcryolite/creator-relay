"""Small, inspectable hand-off boundary for a creator's persistent Mind."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from email.message import EmailMessage
from email.utils import formataddr
from typing import Iterable


@dataclass(frozen=True)
class CreatorBrief:
    """A creator-provided source and preferences, never a fabricated analysis."""

    source: str
    audience: str
    channels: tuple[str, ...]
    goal: str

    def validate(self) -> None:
        if len(self.source.strip()) < 40:
            raise ValueError("source must contain at least 40 characters")
        if not self.audience.strip():
            raise ValueError("audience is required")
        if not self.channels:
            raise ValueError("choose at least one channel")
        if not self.goal.strip():
            raise ValueError("goal is required")


class MindRelay:
    """Builds a transparent email task for a configured Hello Minds identity.

    The class deliberately only builds a message.  Delivery needs a separately
    configured transport, so a demo cannot accidentally claim a live Mind run.
    """

    def __init__(self, mind_email: str | None, mind_id: str | None = None):
        self.mind_email = (mind_email or "").strip()
        self.mind_id = (mind_id or "").strip()

    @property
    def configured(self) -> bool:
        return bool(self.mind_email and self.mind_id)

    def compose(self, brief: CreatorBrief) -> EmailMessage:
        brief.validate()
        if not self.configured:
            raise ValueError("a Mind email and Mind ID must be explicitly configured")

        message = EmailMessage()
        message["To"] = self.mind_email
        message["From"] = formataddr(("Creator Relay", "relay@localhost"))
        message["Subject"] = f"Creator Relay brief · {brief.goal.strip()}"
        channel_list = ", ".join(brief.channels)
        message.set_content(
            "You are the creator's persistent relay Mind.\n\n"
            f"Mind ID: {self.mind_id}\n"
            f"Audience: {brief.audience.strip()}\n"
            f"Channels: {channel_list}\n"
            f"Goal: {brief.goal.strip()}\n\n"
            "Source material:\n"
            f"{brief.source.strip()}\n\n"
            "Return: one channel-specific hook, a short post outline, and one "
            "follow-up task that preserves the creator's stated preferences."
        )
        return message

    @staticmethod
    def local_preview(brief: CreatorBrief) -> list[dict[str, str]]:
        """Show deterministic draft cards without implying an AI/Mind response."""
        brief.validate()
        excerpt = " ".join(brief.source.split())[:140]
        return [
            {
                "channel": channel,
                "status": "local draft — needs Mind response",
                "hook": f"For {brief.audience}: {brief.goal}.",
                "source_excerpt": excerpt,
            }
            for channel in brief.channels
        ]


def channels(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(value.strip() for value in values if value.strip())
