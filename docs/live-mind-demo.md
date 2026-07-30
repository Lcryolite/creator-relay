# Live Mind demo checklist

This is an evidence checklist for the Creative Minds Jam, not a claim that a
Mind has been created or contacted.

## Confirmed platform facts

Hello Minds' public documentation states that users communicate with a Mind by
email or Telegram. A Mind-to-Mind Circle can be introduced by sending an email
and CC'ing the other Mind. Unknown senders are blocked, so the owner should
first introduce their own sender identity to the Mind in Hello Minds.

## Before recording

1. In Hello Minds, create the product Mind and save its **Mind ID** and **Mind
   Email**. Add those required details to the DoraHacks application only after
   reviewing the platform's fields.
2. Make the owner's email an allowed/introduced correspondent for that Mind.
3. Run Creator Relay with only local environment variables:

   ```bash
   CREATOR_RELAY_MIND_ID='actual-mind-id' \
   CREATOR_RELAY_MIND_EMAIL='actual-mind-email' \
   .venv/bin/creator-relay
   ```

4. Create a brief in the local UI. It records the creator's stated audience,
   goal, channels and a queued follow-up visibly in the timeline.
5. Use `MindRelay.compose()` or an owner-approved mail client to send the
   generated brief to the actual Mind email. Do not record credentials or
   private email contents.

## What the video needs to prove

Use separate, truthful clips to show:

- **Memory:** the Mind recalls a prior creator preference from an earlier
  message.
- **Continuity:** it carries that preference into the next channel brief.
- **Autonomous follow-up:** it sends or schedules a meaningful follow-up
  without the creator repeating the original goal.
- **Product connection:** the Creator Relay timeline and the Mind response
  refer to the same creator brief; no made-up response is shown.

The 1.5–2 minute DoraHacks video should state any local-only components and
show the live Mind interaction directly.
