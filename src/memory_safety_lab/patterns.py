"""Sensitive-data detectors used before agent memories are persisted."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    label: str
    value: str


PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[REDACTED_EMAIL]"),
    ("phone", re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b"), "[REDACTED_PHONE]"),
    ("api_key", re.compile(r"\b(?:sk|pk|api[_-]?key|api|key|token)\s*[:=_-]?\s*[A-Za-z0-9_-]{12,}\b", re.I), "[REDACTED_KEY]"),
    ("otp", re.compile(r"\b(?:otp|code)\s*[:=-]?\s*\d{4,8}\b", re.I), "[REDACTED_CODE]"),
    ("card", re.compile(r"\b(?:\d[ -]?){13,16}\b"), "[REDACTED_CARD]"),
    ("cookie", re.compile(r"\b(?:sessionid|cookie|auth_token)\s*[:=]\s*[^;\s]+", re.I), "[REDACTED_COOKIE]"),
)

CONFIDENTIAL_MARKERS = (
    "confidential client",
    "nda",
    "private dataset",
    "production credential",
    "internal-only",
)


def detect(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for label, pattern, _replacement in PATTERNS:
        for match in pattern.findall(text):
            value = match if isinstance(match, str) else match[0]
            findings.append(Finding(label, value.strip()))
    lowered = text.lower()
    for marker in CONFIDENTIAL_MARKERS:
        if marker in lowered:
            findings.append(Finding("confidential_marker", marker))
    return findings


def redact(text: str) -> str:
    redacted = text
    for _label, pattern, replacement in PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted
