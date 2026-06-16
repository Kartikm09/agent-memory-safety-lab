"""Command line interface for agent memory safety audits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .auditor import audit_session
from .report import render_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit agent memory and skill candidates.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit = subparsers.add_parser("audit", help="Audit a session JSON file.")
    audit.add_argument("path", type=Path)
    audit.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "audit":
        payload = json.loads(args.path.read_text(encoding="utf-8"))
        audit = audit_session(payload)
        if args.format == "json":
            print(json.dumps(audit.to_dict(), indent=2))
        else:
            print(render_text(audit))
        return 0
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
