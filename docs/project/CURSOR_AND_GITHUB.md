# Cursor + GitHub workflow

Magnus uses **one** Git remote: GitHub.

**Repository:** https://github.com/sakshamgoyal06/magnus-ai

Infrastructure authority: [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md). Build state: [CURRENT_STATE.md](CURRENT_STATE.md).

## Local (desktop or laptop)

```bash
git clone https://github.com/sakshamgoyal06/magnus-ai.git
cd magnus-ai
cp .env.example .env
```

Use normal GitHub auth (`gh auth login`, SSH, or HTTPS credential manager). Push and pull against `origin` only.

## Cursor web / phone (Cloud Agents)

1. Open [Cursor Agents](https://cursor.com/agents) (works in the mobile browser).
2. Start or configure an agent for **`sakshamgoyal06/magnus-ai`** from **GitHub** (not Cursor Origin).
3. In **Cloud Agent environment** settings for this repo:
   - Link the **GitHub** repository `sakshamgoyal06/magnus-ai`.
   - Keep **`GITHUB_TOKEN`** (or rely on Cursor’s GitHub integration) so the agent can `git push`.
4. New agents use `.cursor/environment.json` `install` to run `uv sync --extra dev`.

If an old environment still points at `origin.cursor.com/.../magnus-ai`, create a **new** personal environment tied to the GitHub repo or update the environment’s repository URL in the dashboard so pushes land on GitHub only.

## Secrets

| Secret | Purpose |
|--------|---------|
| `GITHUB_TOKEN` | Push/pull from Cloud Agents when not using integrated GitHub auth |
| `TELEGRAM_BOT_TOKEN` | Optional; enables Telegram polling in `magnus-api` |

Do not commit `.env` or tokens.
