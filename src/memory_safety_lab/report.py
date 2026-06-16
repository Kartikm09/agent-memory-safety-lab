"""Text rendering for memory safety audits."""

from __future__ import annotations

from .auditor import SessionAudit


def render_text(audit: SessionAudit) -> str:
    lines = [
        "Agent Memory Safety Lab",
        f"Session: {audit.session_id}",
        f"Score: {audit.score}/100",
        "",
        "Summary",
    ]
    for key, value in audit.summary.items():
        lines.append(f"- {key}: {value}")

    if audit.memory_candidates:
        lines.extend(["", "Memory Candidates"])
        for item in audit.memory_candidates:
            lines.append(f"{item.decision.upper()} [{item.risk}] {item.redacted_text}")
            lines.append(f"  reason: {', '.join(item.reasons)}")

    if audit.skill_candidates:
        lines.extend(["", "Skill Candidates"])
        for item in audit.skill_candidates:
            lines.append(f"{item.decision.upper()} [{item.risk}] {item.redacted_text}")
            lines.append(f"  reason: {', '.join(item.reasons)}")
    return "\n".join(lines)
