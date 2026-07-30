# Creator Relay

Creator Relay is a local, inspectable prototype for the **Content Repurposing
Across Platforms** Creative Minds JAM track. A creator supplies source material,
audience, goal, and target channels; the app prepares transparent per-channel
draft cards and can compose a structured task for a configured Hello Minds
identity.

## Truthful runtime boundary

The default demo is deliberately offline and does **not** invoke a Mind, send
email, or fabricate an agent response. Its cards are marked `local draft —
needs Mind response`.

For a real contest integration, the owner must:

1. Create a Mind and obtain its Mind ID and Mind Email in Hello Minds.
2. Set `CREATOR_RELAY_MIND_ID` and `CREATOR_RELAY_MIND_EMAIL` only in the local
   runtime environment.
3. Configure an owner-approved message delivery channel and demonstrate the
   actual Mind response in the submission video.

The code's `MindRelay.compose()` boundary makes the requested persistent Mind
task explicit without sending anything by itself.

## Run locally

```bash
python -m venv .venv
.venv/bin/pip install -e . pytest
.venv/bin/pytest -q
.venv/bin/creator-relay
```

Open <http://127.0.0.1:8790>. The server binds to loopback only.

## Why this project

Content creators often repurpose long-form work manually, losing the context of
their voice, audience and prior decisions every time they switch channels. A
real configured Mind is intended to carry those preferences across briefs,
provide follow-up tasks, and remain accountable through an inspectable message
handoff.

## Status

This repository is contest preparation, not an entry. It has no Mind account,
Mind ID, Mind Email, cognition grant, live delivery, submitted video, or
DoraHacks submission.
