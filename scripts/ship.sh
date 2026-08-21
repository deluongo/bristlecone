#!/usr/bin/env bash
# ship.sh — the only sanctioned path to commit+push in this repo.
# Gates: credential-shape scan, local private-context denylist, explicit paths only.
# Usage: scripts/ship.sh -m "message" [--trailer "Key: value"]... path [path...]
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

msg="" ; trailers=() ; paths=()
while [ $# -gt 0 ]; do
  case "$1" in
    -m) msg="$2"; shift 2;;
    --trailer) trailers+=("$2"); shift 2;;
    *) paths+=("$1"); shift;;
  esac
done
[ -n "$msg" ] || { echo "ship.sh: -m message required" >&2; exit 3; }
[ ${#paths[@]} -gt 0 ] || { echo "ship.sh: explicit paths required (never add -A)" >&2; exit 3; }

# Gate 1: credential shapes across the whole tree (same patterns as CI hygiene).
pats=('[s]k-ant-' '[g]hp_[A-Za-z0-9]{20,}' '[g]ithub_pat_' '[A]GE-SECRET-KEY' '[s]k-[A-Za-z0-9]{20,}' '[A]KIA[0-9A-Z]{16}' '[A-Za-z0-9+/]{200,}')
for p in "${pats[@]}"; do
  if git grep -I -qE "$p" -- ':!/.github/workflows/hygiene.yml' 2>/dev/null; then
    echo "ship.sh: BLOCKED — credential-shaped content matches: $p" >&2; exit 2
  fi
done

# Gate 2: local private-context denylist (gitignored on purpose — a public list would leak what it protects).
if [ -f denylist.local.txt ]; then
  while IFS= read -r term; do
    [ -z "$term" ] && continue
    case "$term" in \#*) continue;; esac
    if git grep -I -qiF "$term" -- ':!denylist.local.txt' 2>/dev/null; then
      echo "ship.sh: BLOCKED — private-context term found in tracked files (see denylist.local.txt)" >&2; exit 2
    fi
  done < denylist.local.txt
else
  echo "ship.sh: WARNING — denylist.local.txt missing; private-context gate skipped" >&2
fi

git add -- "${paths[@]}"
full="$msg"
for t in "${trailers[@]:-}"; do [ -n "$t" ] && full="$full
$t"; done
git commit -m "$full"
git push
