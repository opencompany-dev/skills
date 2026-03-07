---
name: slack
description: Read Slack channels, threads, users, and message search through Platform Gateway read-only actions.
---

# Slack (Read-Only)

Inspect Slack workspace data.

## Capabilities

- List channels
- Read channel history
- Read thread replies
- List users
- Search messages

## Notes

- All requests run through Platform Gateway.
- Write operations are intentionally unavailable.
- Use channel IDs for deterministic reads.
