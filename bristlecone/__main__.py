"""CLI entry point. Exit-code contract: 0 = success (validate: all records
valid), 1 = findings, 2 = usage, path, or git error.

Usage: python -m bristlecone validate [--strict] PATH...
       python -m bristlecone validate --git-range BASE..HEAD [--repo DIR]
       python -m bristlecone render RECORDS_DIR --out OUT_DIR [--stamps]
       python -m bristlecone lanes [--config lanes.toml]
       python -m bristlecone ask RECORD [--config lanes.toml] [--lanes NAMES]
                                        [--dry-run [--out PATH]] [--denylist PATH]

For `ask`, a config that cannot be loaded is a usage-class error (2), unlike
`lanes` where the config is itself the subject under validation (1).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import ask, gitio, laneconfig, records, render, scrub, validate


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
    lanes_parser = subparsers.add_parser(
        "lanes", help="validate and list the lane config (fail-closed)"
    )
    lanes_parser.add_argument(
        "--config", type=Path, default=Path("lanes.toml"), help="lane config (default: lanes.toml)"
    )
    ask_parser = subparsers.add_parser(
        "ask",
        help="fan an open record's question out to lanes and fill attributed "
        "positions (never creates or decides a record)",
    )
    ask_parser.add_argument("record", type=Path, metavar="RECORD")
    ask_parser.add_argument(
        "--config", type=Path, default=Path("lanes.toml"), help="lane config (default: lanes.toml)"
    )
    ask_parser.add_argument(
        "--lanes", metavar="NAME[,NAME...]", help="subset of configured lanes (default: all)"
    )
    ask_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="deterministic fixtures, no transport; the record file is never written",
    )
    ask_parser.add_argument(
        "--out", type=Path, help="dry-run only: write the would-be updated record here"
    )
    ask_parser.add_argument(
        "--denylist",
        type=Path,
        default=Path("denylist.local.txt"),
        help="local denylist for the scrub gates (absent file = no terms)",
    )
    args = parser.parse_args(argv)
    commands = {
        "validate": _cmd_validate,
        "render": _cmd_render,
        "lanes": _cmd_lanes,
        "ask": _cmd_ask,
    }
    return commands[args.command](args)


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


def _cmd_lanes(args: argparse.Namespace) -> int:
    if not args.config.is_file():
        print(f"bristlecone: no such file: {args.config}", file=sys.stderr)
        return 2
    try:
        lanes = laneconfig.load(args.config)
    except laneconfig.ConfigError as exc:
        print(f"bristlecone: {exc}", file=sys.stderr)
        return 1
    for lane in lanes:
        spend = "metered -> declined:gate (KEY-HANDLING gate closed)" if lane.metered else "$0"
        print(f"{lane.name:<10} {lane.kind:<12} {lane.vendor}/{lane.model} [{lane.route}] {spend}")
    print(f"OK: {len(lanes)} lane(s) valid")
    return 0


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


def _cmd_ask(args: argparse.Namespace) -> int:
    if args.out and not args.dry_run:
        print("bristlecone: --out is dry-run only (real runs update RECORD in place)",
              file=sys.stderr)
        return 2
    try:
        lane_list = _selected_lanes(args)
        record = records.load_file(args.record)
    except (OSError, laneconfig.ConfigError, records.RecordParseError, LookupError) as exc:
        print(f"bristlecone: {exc}", file=sys.stderr)
        return 2
    denylist = scrub.load_denylist(args.denylist)
    try:
        result = ask.run_ask(record, lane_list, denylist, dry_run=args.dry_run)
    except ask.AskError as exc:
        print(f"bristlecone: {exc}", file=sys.stderr)
        return 2
    except ask.OutboundBlocked as exc:
        print(f"bristlecone: {exc} — nothing was dispatched", file=sys.stderr)
        return 1
    return _finish_ask(args, result)


def _selected_lanes(args: argparse.Namespace) -> tuple[laneconfig.Lane, ...]:
    lane_list = laneconfig.load(args.config)
    if not args.lanes:
        return lane_list
    by_name = {lane.name: lane for lane in lane_list}
    try:
        return tuple(by_name[name] for name in args.lanes.split(","))
    except KeyError as exc:
        raise LookupError(f"no lane named {exc.args[0]!r} in {args.config}") from exc


def _finish_ask(args: argparse.Namespace, result: ask.AskResult) -> int:
    for report in result.reports:
        hits = ",".join(report.hits) or "-"
        print(f"{report.lane:<10} {report.status:<26} stance={report.stance or '-'} scrub={hits}")
    if args.dry_run:
        if args.out:
            args.out.write_text(result.text, encoding="utf-8")
            print(f"dry-run: assembled record written to {args.out} (RECORD untouched)")
        else:
            print("dry-run: RECORD untouched (use --out PATH to inspect the assembled record)")
    else:
        args.record.write_text(result.text, encoding="utf-8")
        print(f"updated {args.record}")
    return 0 if result.all_filled else 1


if __name__ == "__main__":
    sys.exit(main())
