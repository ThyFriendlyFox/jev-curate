#!/usr/bin/env bash
# The Ralph loop: run the same short prompt against the repo, over and over,
# until the goal in ralph/GOAL.md is proven by ./verify/verify.sh.
#
#   ralph/loop.sh                 # up to RALPH_MAX_ITERATIONS (default 10)
#   RALPH_MAX_ITERATIONS=3 ralph/loop.sh
#   RALPH_AGENT_CMD='claude -p --permission-mode acceptEdits' ralph/loop.sh
#
# Exit codes: 0 goal proven · 1 verify still red after max iterations ·
# 2 agent wrote ralph/BLOCKED.md · 3 agent command failed.
set -uo pipefail
cd "$(dirname "$0")/.."

MAX="${RALPH_MAX_ITERATIONS:-10}"
AGENT="${RALPH_AGENT_CMD:-claude -p --permission-mode acceptEdits}"
PROMPT="$(cat ralph/PROMPT.md)"
mkdir -p ralph/runs
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
log="ralph/runs/$stamp.log"

verify() { ./verify/verify.sh >>"$log" 2>&1; }

echo "ralph: start $stamp, max $MAX iterations, log $log"
if verify; then
  echo "ralph: goal already proven (verify green at $(git rev-parse --short HEAD))"
  exit 0
fi

for ((i = 1; i <= MAX; i++)); do
  rm -f ralph/BLOCKED.md
  echo "ralph: iteration $i/$MAX" | tee -a "$log"
  if ! printf '%s\n' "$PROMPT" | $AGENT >>"$log" 2>&1; then
    echo "ralph: agent command failed on iteration $i (see $log)"; exit 3
  fi
  if [[ -f ralph/BLOCKED.md ]]; then
    echo "ralph: blocked on iteration $i:"; cat ralph/BLOCKED.md; exit 2
  fi
  if verify; then
    echo "ralph: goal proven on iteration $i (verify green at $(git rev-parse --short HEAD))"
    exit 0
  fi
  echo "ralph: verify still red after iteration $i" | tee -a "$log"
done

echo "ralph: max iterations reached; verify still red (see $log)"
exit 1
