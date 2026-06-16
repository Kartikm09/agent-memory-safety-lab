---
name: memory-safety-auditor
description: Audit proposed AI agent memory entries and reusable skill candidates for sensitive data, redaction needs, durability, and safe persistence decisions.
---

# Memory Safety Auditor

Use this skill when deciding whether a session observation should become long-term agent memory or reusable skill guidance.

## Workflow

1. Separate durable profile or workflow facts from temporary page/session details.
2. Detect emails, phones, API keys, OTPs, card-like numbers, cookies, and confidential markers.
3. Block credentials, OTPs, payment data, cookies, and production secrets.
4. Redact contact details if the surrounding statement is useful but too identifying.
5. Allow stable user preferences, durable project context, and reusable working patterns.
6. Promote process-heavy observations into skill candidates only when they describe repeatable steps.
7. Return a decision of allow, redact, block, or temporary with a short reason.

## Output

Return a compact audit table with the original intent, redacted preview, decision, risk, and reason.
