# Cursor Cloud Agents

Use this repo from [Cursor Agents](https://cursor.com/agents) (desktop, web, or mobile).

## Setup

1. Start or configure an agent for **`sakshamgoyal06/magnus-ai`** linked to the GitHub repository.
2. In **Cloud Agent environment** settings:
   - Attach the GitHub repository `sakshamgoyal06/magnus-ai`.
   - Provide **`GITHUB_TOKEN`** (or use Cursor’s GitHub integration) so the agent can push.
3. On boot, `.cursor/environment.json` runs `uv sync --extra dev`.

Local clone and API setup are in the [README](../README.md).

## Secrets

| Secret | Purpose |
|--------|---------|
| `GITHUB_TOKEN` | Push/pull from Cloud Agents when not using integrated GitHub auth |
| `TELEGRAM_BOT_TOKEN` | Optional; enables Telegram polling in `magnus-api` |

Do not commit `.env` or tokens.
