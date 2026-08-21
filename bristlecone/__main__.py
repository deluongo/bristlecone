"""CLI entry point. Exit-code contract: 0 = success (validate: all records
valid), 1 = findings, 2 = usage, path, or git error.

Usage: python -m bristlecone validate [--strict] PATH...
       python -m bristlecone validate --git-range BASE..HEAD [--repo DIR]
       python -m bristlecone render RECORDS_DIR --out OUT_DIR [--stamps]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import gitio, records, render, validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bristlecone")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser(
        "validate", help="fail-closed validation of record files or trees"
    )
    validate_parser.add_argument("paths", nargs="*", type=Path, metavar="PATH")
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="also require full attribution on tool-filled positions",
    )
    validate_parser.add_argument(
        "--git-range",
        metavar="BASE..HEAD",
        help="instead of validating files, enforce spec §4 append-only semantics "
        "across a commit range (BASE...HEAD diffs from the merge base)",
    )
    validate_parser.add_argument(
        "--repo", type=Path, default=Path("."), help="repository for --git-range (default: .)"
    )
    render_parser = subparsers.add_parser(
        "render", help="render a record tree to static HTML (lenient: content never fails it)"
    )
    render_parser.add_argument("root", type=Path, metavar="RECORDS_DIR")
    render_parser.add_argument("-o", "--out", type=Path, required=True, metavar="OUT_DIR")
    render_parser.add_argument(
        "--stamps",
        action="store_true",
        help="stamp pages with first-introduced commits (spec §4); RECORDS_DIR must be in a repo",
    )
    args = parser.parse_args(argv)
    return _cmd_validate(args) if args.command == "validate" else _cmd_render(args)


def _cmd_validate(args: argparse.Namespace) -> int:
    if args.git_range:
        return _cmd_validate_range(args)
    if not args.paths:
        print("bristlecone: validate needs PATH arguments or --git-range", file=sys.stderr)
        return 2
    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(records.scan_tree(path))
        elif path.is_file():
            files.append(path)
        else:
            print(f"bristlecone: no such path: {path}", file=sys.stderr)
            return 2
    if _report(validate.validate_files(files, strict=args.strict)):
        return 1
    print(f"OK: {len(files)} record(s) valid")
    return 0


def _cmd_validate_range(args: argparse.Namespace) -> int:
    if args.paths:
        print("bristlecone: --git-range takes no PATH arguments", file=sys.stderr)
        return 2
    try:
        findings = gitio.check_range(args.repo, args.git_range)
    except gitio.GitError as exc:
        print(f"bristlecone: {exc}", file=sys.stderr)
        return 2
    if _report(findings):
        return 1
    print(f"OK: append-only semantics hold across {args.git_range}")
    return 0


def _report(findings: list[validate.Finding]) -> bool:
    for finding in findings:
        print(f"{finding.record}: {finding.code}: {finding.message}")
    if findings:
        print(f"{len(findings)} finding(s)")
    return bool(findings)


def _cmd_render(args: argparse.Namespace) -> int:
    if not args.root.is_dir():
        print(f"bristlecone: no such directory: {args.root}", file=sys.stderr)
        return 2
    stamps = built_from = None
    if args.stamps:
        try:
            stamps = gitio.first_commit_stamps(args.root, records.scan_tree(args.root))
            built_from = gitio.head_commit(args.root)
        except gitio.GitError as exc:
            print(f"bristlecone: {exc}", file=sys.stderr)
            return 2
    written = render.render_tree(args.root, args.out, stamps=stamps, built_from=built_from)
    print(f"rendered {len(written) - 1} record page(s) + index -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
