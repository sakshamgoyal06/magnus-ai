# CrewAI 2.0

A [CrewAI](https://crewai.com) **2.x JSON-first** project: agents live in `agents/*.jsonc`, tasks and crew settings in `crew.jsonc`, and `crewai run` loads that definition directly.

This repo ships a two-agent **research crew** that gathers information on a topic and writes a markdown report to `output/report.md`.

## Prerequisites

- Python 3.10–3.13
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- [CrewAI CLI](https://docs.crewai.com/en/installation): `uv tool install crewai`

## Setup

```bash
cp .env.example .env
# Add OPENAI_API_KEY and SERPER_API_KEY (for web search)
crewai install
```

## Run

```bash
crewai run
```

Default input topic is set in `crew.jsonc` under `inputs`. Change `topic` there, or remove it to be prompted at runtime.

## Project layout

```text
├── agents/
│   ├── researcher.jsonc
│   └── analyst.jsonc
├── crew.jsonc
├── knowledge/          # optional knowledge files
├── skills/             # optional agent skills
├── tools/              # custom tools (custom:<name>)
├── output/             # generated report
├── pyproject.toml
└── .env
```

## Customize

- Edit agent roles, goals, and models in `agents/*.jsonc`
- Edit task flow, memory, and inputs in `crew.jsonc`
- Add built-in tools (e.g. `FileReadTool`) or `custom:my_tool` entries pointing at `tools/my_tool.py`

See the [first crew guide](https://docs.crewai.com/en/guides/crews/first-crew) for more.

## Security

`custom:` tools and Python callbacks in JSON execute local code when the crew loads. Only run projects from sources you trust.
