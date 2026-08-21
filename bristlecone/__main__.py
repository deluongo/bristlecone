"""CLI entry point. Exit-code contract: 0 = all records valid, 1 = findings,
2 = usage or path error. Usage: python -m bristlecone validate [--strict] PATH...
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import records, validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bristlecone")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser(
        "validate", help="fail-closed validation of record files or trees"
    )
    validate_parser.add_argument("paths", nargs="+", type=Path, metavar="PATH")
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="also require full attribution on tool-filled positions",
    )
    args = parser.parse_args(argv)
    return _cmd_validate(args)


def _cmd_validate(args: argparse.Namespace) -> int:
    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(records.scan_tree(path))
        elif path.is_file():
            files.append(path)
        else:
            print(f"bristlecone: no such path: {path}", file=sys.stderr)
            return 2
    findings = validate.validate_files(files, strict=args.strict)
    for finding in findings:
        print(f"{finding.record}: {finding.code}: {finding.message}")
    if findings:
        print(f"{len(findings)} finding(s) across {len(files)} file(s)")
        return 1
    print(f"OK: {len(files)} record(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
