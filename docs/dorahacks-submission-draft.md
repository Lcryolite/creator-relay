# DoraHacks submission draft — Creator Relay

> Status: draft only. Replace every `[LIVE EVIDENCE REQUIRED]` item with a
> truthful link, clip, or configuration fact before submitting.

## Project name

Creator Relay — persistent cross-platform continuity for independent creators

## Track

Content Repurposing Across Platforms

## One-line description

Creator Relay turns a creator-owned long-form brief into channel-specific
publication tasks while preserving the audience, tone and follow-up intent that
the creator established in earlier sessions.

## The creator problem

Independent creators rarely publish in one place. A video, newsletter or live
stream becomes a YouTube description, an X thread, an Instagram caption and a
community update. Each adaptation normally restarts the conversation: the
creator repeats their audience, voice, launch goal and prior decisions. That
cost makes cross-posting inconsistent and removes time from the work that only
the creator can do.

## What we built

Creator Relay is a loopback-first Flask application with an inspectable
continuity timeline. A creator adds source material, audience, objective and
target channels. The app stores that stated context and queues a visible
follow-up rather than hiding it in an opaque prompt history.

The production handoff is a persistent **Minds by Animoca Brands** agent. The
application composes a structured email task addressed to a configured Mind ID
and Mind Email. The Mind is responsible for recalling the earlier preference,
continuing the creator's campaign, and proactively returning the next action.
The public repository deliberately has no default credentials and never
pretends a local preview is a Mind response.

## Minds integration

1. The owner creates a dedicated Creator Relay Mind in Hello Minds and
   introduces the creator's sender address.
2. Creator Relay retains a visible record of the creator's brief and scheduled
   follow-up, then composes a task for that Mind's real email identity.
3. The Mind receives the email through its supported email channel, uses its
   persistent memory to retain the creator's preferences, and returns a
   channel-specific continuation.
4. The follow-up is recorded and demonstrated over a second session.

`[LIVE EVIDENCE REQUIRED: Mind ID/email visible only as safely redacted proof,
first request, later preference recall, and autonomous follow-up clip.]`

## What is in the repository

- loopback-only Flask interface;
- SQLite timeline showing the exact context a creator asked to retain;
- deterministic local draft cards clearly marked as not a Mind response;
- a fail-closed SMTP handoff command requiring explicit confirmation and
  owner-local credentials;
- unit tests and public GitHub Actions verification;
- a live-demo checklist that separates local preparation from a genuine Mind
  interaction.

Repository: https://github.com/Lcryolite/creator-relay

## 1.5–2 minute video storyboard

| Time | Screen / action | Claim permitted |
| --- | --- | --- |
| 0:00–0:15 | Explain creator's cross-posting context loss. | The problem and intended outcome. |
| 0:15–0:35 | Submit a real creator-owned brief to Creator Relay. | Local UI stores creator-provided context. |
| 0:35–0:50 | Open the timeline and show the queued follow-up. | Visible local continuity record, not a Mind run. |
| 0:50–1:15 | Show the actual configured Mind email and a sent task. | `[LIVE EVIDENCE REQUIRED]` |
| 1:15–1:40 | In a later interaction, show the Mind recalling a stated preference. | `[LIVE EVIDENCE REQUIRED]` |
| 1:40–1:55 | Show proactive follow-up and the resulting channel continuation. | `[LIVE EVIDENCE REQUIRED]` |
| 1:55–2:00 | Point to repository, test status and future creator workflow. | Public source and actual verified state. |

## Judging-criteria mapping

| Criterion | Evidence to submit |
| --- | --- |
| Minds Integration Depth | Two-session email interaction showing memory, plus autonomous follow-up. `[LIVE EVIDENCE REQUIRED]` |
| Creator-Economy Problem Fit | The problem statement and one creator-owned source brief. |
| Innovation & Creativity | Transparent local-to-persistent-agent handoff; preferences are inspectable. |
| Execution & Completeness | Public code, working local UI, tests, and live Mind sequence. `[LIVE EVIDENCE REQUIRED]` |
| Viability & Scalability | Email-first workflow can serve creators without additional client installation. |

## Submission checklist

- [ ] Register as Hacker for this specific DoraHacks event.
- [ ] Create/configure a Mind and obtain actual Mind ID + Mind Email.
- [ ] Obtain/confirm cognition grant if approved.
- [ ] Produce the real two-session Mind evidence above.
- [ ] Record 1.5–2 minute English video and upload a public link.
- [ ] Add repository URL and technical documentation.
- [ ] Verify every statement against the final runtime before submitting.
