"""Audit proposed memory and skill candidates from agent sessions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .patterns import detect, redact

STABLE_MEMORY_MARKERS = (
    "prefers",
    "usually",
    "always",
    "avoid",
    "likes",
    "workflow",
    "project context",
    "profile context",
)

SKILL_MARKERS = (
    "when",
    "use",
    "steps",
    "workflow",
    "validate",
    "run",
    "check",
    "rubric",
)


@dataclass(frozen=True)
class CandidateAudit:
    text: str
    decision: str
    risk: str
    redacted_text: str
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.redacted_text,
            "decision": self.decision,
            "risk": self.risk,
            "redacted_text": self.redacted_text,
            "reasons": self.reasons,
        }


@dataclass(frozen=True)
class SessionAudit:
    session_id: str
    score: int
    memory_candidates: list[CandidateAudit]
    skill_candidates: list[CandidateAudit]
    summary: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "score": self.score,
            "summary": self.summary,
            "memory_candidates": [item.to_dict() for item in self.memory_candidates],
            "skill_candidates": [item.to_dict() for item in self.skill_candidates],
        }


def audit_session(payload: dict[str, Any]) -> SessionAudit:
    memory_candidates = [_audit_candidate(str(item), kind="memory") for item in payload.get("memory_candidates", [])]
    skill_candidates = [_audit_candidate(str(item), kind="skill") for item in payload.get("skill_candidates", [])]
    all_candidates = memory_candidates + skill_candidates
    total = max(1, len(all_candidates))
    safe_points = sum(_points(item) for item in all_candidates)
    score = round(safe_points / (total * 10) * 100)
    summary = {
        "allow": sum(1 for item in all_candidates if item.decision == "allow"),
        "redact": sum(1 for item in all_candidates if item.decision == "redact"),
        "block": sum(1 for item in all_candidates if item.decision == "block"),
        "temporary": sum(1 for item in all_candidates if item.decision == "temporary"),
    }
    return SessionAudit(str(payload.get("session_id", "unknown-session")), score, memory_candidates, skill_candidates, summary)


def _audit_candidate(text: str, kind: str) -> CandidateAudit:
    findings = detect(text)
    lowered = text.lower()
    reasons: list[str] = []

    if findings:
        labels = sorted({finding.label for finding in findings})
        reasons.extend(f"contains {label}" for label in labels)
        decision = "block" if {"api_key", "otp", "card", "cookie"} & set(labels) else "redact"
        risk = "high" if decision == "block" else "medium"
        return CandidateAudit(text, decision, risk, redact(text), reasons)

    if kind == "memory":
        if any(marker in lowered for marker in STABLE_MEMORY_MARKERS):
            return CandidateAudit(text, "allow", "low", text, ["stable preference or durable project context"])
        return CandidateAudit(text, "temporary", "low", text, ["not durable enough for long-term memory"])

    if kind == "skill":
        marker_count = sum(1 for marker in SKILL_MARKERS if marker in lowered)
        if marker_count >= 2 and len(text.split()) >= 8:
            return CandidateAudit(text, "allow", "low", text, ["reusable process guidance"])
        return CandidateAudit(text, "temporary", "low", text, ["too narrow for reusable skill guidance"])

    return CandidateAudit(text, "temporary", "low", text, ["unknown candidate type"])


def _points(item: CandidateAudit) -> int:
    if item.decision == "allow":
        return 10
    if item.decision == "temporary":
        return 8
    if item.decision == "redact":
        return 6
    return 0
