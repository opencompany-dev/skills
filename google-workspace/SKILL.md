---
name: google-workspace
description: Read Google Workspace data (Gmail, Calendar, Drive) via the Google Workspace CLI through Platform Gateway.
---

# Google Workspace (Read-Only)

This skill uses the Google Workspace CLI backend for read operations.

## Required setup

- Install CLI:
  - `npm i -g @googleworkspace/cli`
- Optional skills install reference:
  - `npx skills add github:googleworkspace/cli`

## Available actions

- Gmail: list/get messages
- Calendar: list events
- Drive: list files

## Constraints

- Read-only actions only.
- Gateway allowlist blocks write verbs at runtime.
