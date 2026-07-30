# Creator Relay

Creator Relay is a local, inspectable prototype for the **Content Repurposing
Across Platforms** Creative Minds JAM track. A creator supplies source material,
audience, goal, and target channels; the app prepares transparent per-channel
draft cards and can compose a structured task for a configured Hello Minds
identity.

## Truthful runtime boundary

The default demo is deliberately offline and does **not** invoke a Mind, send
email, or fabricate an agent response. Its cards are marked `local draft —
needs Mind response`. Each brief is stored in a visible local SQLite timeline
with a queued next-day follow-up, so the creator can inspect continuity rather
than trust hidden state. This local timeline is preparation evidence, not proof
of a Minds run.

For a real contest integration, the owner must:

1. Create a Mind and obtain its Mind ID and Mind Email in Hello Minds.
2. Set `CREATOR_RELAY_MIND_ID` and `CREATOR_RELAY_MIND_EMAIL` only in the local
   runtime environment.
3. Configure an owner-approved message delivery channel and demonstrate the
   actual Mind response in the submission video.

The code's `MindRelay.compose()` boundary makes the requested persistent Mind
task explicit without sending anything by itself.

See [the live Mind demo checklist](docs/live-mind-demo.md) for the official
email/Telegram integration facts and a truthful recording sequence.
The [DoraHacks submission draft](docs/dorahacks-submission-draft.md) contains
the English description, criteria mapping and video storyboard with live-only
evidence marked explicitly.

## Live email delivery (owner-only)

The web UI never delivers email. A separate CLI command is intentionally
fail-closed: it needs an explicit `--confirm-live-delivery`, a real Mind ID and
Mind Email, and locally injected SMTP values. It does not read ambient Gmail
browser state or place credentials in the repository.

```bash
CREATOR_RELAY_SMTP_HOST='smtp.example.com' \
CREATOR_RELAY_SMTP_USERNAME='owner@example.com' \
CREATOR_RELAY_SMTP_PASSWORD='local-app-password' \
CREATOR_RELAY_SMTP_FROM='owner@example.com' \
.venv/bin/creator-relay send-mind-brief \
  --confirm-live-delivery --mind-id 'actual-mind-id' \
  --mind-email 'actual-mind-email' --channels 'YouTube,X' \
  --audience 'independent video creators' \
  --goal 'invite discussion around the next episode' \
  --source 'At least forty characters of creator-owned source material.'
```

This command is not run by this repository's tests or demo.

## KeeperHub testnet execution receipts

Creator Relay can also let an agent create an auditable **testnet** community
reward receipt through KeeperHub's documented Direct Execution API. It only
accepts Ethereum Sepolia (`11155111`) and Base Sepolia (`84532`), always starts
with a dry-run simulation, and requires an explicit owner-supplied `kh_`
organization API key. The repository never sends a transfer by default.

```bash
KEEPERHUB_API_KEY='kh_owner_local_only' \
.venv/bin/creator-relay simulate-community-reward \
  --chain-id 11155111 \
  --recipient '0x0000000000000000000000000000000000000001' \
  --amount '0.01'
```

This is preparation for the KeeperHub hackathon, not evidence of a real
transaction. A broadcast path remains disabled in the CLI until a separate
owner-confirmed execution is intentionally added and recorded.

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
