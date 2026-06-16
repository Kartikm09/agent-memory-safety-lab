# Agent Memory Safety Lab

Safety harness for agent memory, skill distillation, and profile-safe knowledge capture.

This repository audits proposed memory entries from AI assistant sessions and decides whether each item is:

- Safe to persist
- Needs redaction
- Better suited as a temporary note
- A candidate for reusable skill guidance
- Blocked because it contains sensitive data

The lab is built around public-safe examples and a dependency-free Python CLI.

## Why It Exists

Agentic systems increasingly learn from user sessions, tool traces, and completed workflows. That creates a new QA problem: memory can make agents smarter, but careless memory can store private contact details, credentials, client names, or confidential project information.

This project demonstrates a practical audit layer before session observations become long-term memory.

## Quick Start

```bash
PYTHONPATH=src python3 -m memory_safety_lab.cli audit examples/session.json
```

JSON output:

```bash
PYTHONPATH=src python3 -m memory_safety_lab.cli audit examples/session.json --format json
```

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## What It Checks

- Emails, phone numbers, API keys, tokens, OTPs, and card-like data
- Confidential client or vendor mentions
- Memory entries that are too specific to one private user session
- Skill candidates that contain reusable process knowledge
- Redacted preview text for safer review

## Example Output

```text
Agent Memory Safety Lab
Session: synthetic-agent-session-001
Score: 83/100

ALLOW: Prefer concise QA scorecards for voice-agent evaluation.
REDACT: User contact is [REDACTED_EMAIL].
BLOCK: API token used during setup.
SKILL: Use rubric-first scoring before writing profile-safe summaries.
```

## Portfolio Signal

This project demonstrates:

- Agent memory safety
- AI assistant QA
- Red-team thinking for data persistence
- Skill distillation
- PII redaction
- Python CLI tooling

## Public-Safe Note

All examples are synthetic. Do not place real secrets, private client data, OTPs, cookies, or production session logs in this repository.
