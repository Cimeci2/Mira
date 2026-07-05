"""Stage 3 dispatch — takedown SKILLS, one per target channel.

A skill is the playbook for a takedown route: which channel, whom to notify, and a
prompt (Agents/prompts/takedown_{name}.md) that later drives Gemini Computer Use to
fill that channel's form. Which skill runs comes from the victim's chosen action paths
(wireframe: report to platform / contact host / official complaint) — for now we default
to the EU/FR legal route (the current focus).

Demo dispatch is an email to the DEMO inbox only (G-12) — never a real platform or
authority. The skill still selects the framing/recipient; the real per-site form
submission (Computer Use) plugs in behind submit() later, driven by skill.playbook.
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

import httpx

from . import prompts
from .types import ForensicRecord, Mandate

_RESEND_ENDPOINT = "https://api.resend.com/emails"


@dataclass(frozen=True)
class Skill:
    name: str
    label: str    # human label shown in the notice/event
    channel: str  # official_portal | platform_form | email
    target: str   # real target (portal URL or abuse contact); demo routes to the demo inbox

    @property
    def playbook(self) -> str:
        """The Computer Use playbook for this skill (Agents/prompts/takedown_{name}.md)."""
        return prompts.load(f"takedown_{self.name}")


_SKILLS: dict[str, Skill] = {
    "legal_fr": Skill(
        "legal_fr", "Signalement légal France/UE", "official_portal",
        "https://www.internet-signalement.gouv.fr",
    ),
    "meta": Skill(
        "meta", "Meta (Facebook/Instagram)", "platform_form",
        "https://www.facebook.com/help/contact/1380418588640631",
    ),
    "google": Skill(
        "google", "Google (removal)", "platform_form",
        "https://support.google.com/websearch/troubleshooter/3111061",
    ),
    "x": Skill("x", "X (Twitter)", "platform_form", "https://help.x.com/forms"),
    "host": Skill("host", "Hébergeur / abuse", "email", "abuse@"),
}

DEFAULT_SKILL = "legal_fr"  # focus: EU/FR legal route


def skills() -> dict[str, Skill]:
    return dict(_SKILLS)


def resolve_skill(record: ForensicRecord, mandate: Mandate) -> Skill:
    """Pick the takedown skill for this case. TODO: derive from the victim's chosen
    action paths (wireframe p2) + the detected host. For now: MIRA_TAKEDOWN_SKILL env
    override, else the EU/FR legal route."""
    name = os.getenv("MIRA_TAKEDOWN_SKILL", DEFAULT_SKILL)
    return _SKILLS.get(name, _SKILLS[DEFAULT_SKILL])


def is_configured() -> bool:
    """True when a real dispatch can happen (Resend key + a demo inbox to send to)."""
    return bool(os.getenv("RESEND_API_KEY") and os.getenv("DEMO_TARGET_INBOX"))


async def submit(notice: str, record: ForensicRecord, mandate: Mandate) -> tuple[bool, Skill]:
    """Dispatch the confirmed notice via the resolved skill, to the demo inbox only
    (G-12). Returns (sent, skill): sent=False when unconfigured (caller falls back to a
    mock NOTIFIED so the demo runs keyless). Raises on a real send failure."""
    skill = resolve_skill(record, mandate)
    if not is_configured():
        return False, skill
    subject = f"[{skill.label}] Retrait de contenu illicite — {record.source_url}"
    await asyncio.to_thread(_send_email, subject, notice)
    return True, skill


def _send_email(subject: str, body: str) -> None:
    key = os.getenv("RESEND_API_KEY")
    inbox = os.getenv("DEMO_TARGET_INBOX")
    # Resend requires a verified sender domain; onboarding@resend.dev works in test mode.
    sender = os.getenv("NOTICE_SENDER_EMAIL") or "onboarding@resend.dev"
    resp = httpx.post(
        _RESEND_ENDPOINT,
        headers={"Authorization": f"Bearer {key}"},
        json={"from": sender, "to": [inbox], "subject": subject, "text": body},
        timeout=30,
    )
    resp.raise_for_status()
