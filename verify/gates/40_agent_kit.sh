#!/usr/bin/env bash
# Gate: the agent kit is installed (no placeholders) and the roadmap has a
# ready queue (agent-kit/SETUP.md step 4, ROADMAP.md rules).
set -euo pipefail
cd "$(dirname "$0")/../.."
hits="$(grep -rnoE '\{\{[A-Z_]+\}\}' --exclude=SETUP.md agent-kit ralph .claude AGENTS.md CLAUDE.md 2>/dev/null || true)"
if [[ -n "$hits" ]]; then
  echo "$hits"; echo "placeholders remain in the agent kit"; exit 1
fi
ready=$(grep -cE '^\- \*\*Status:\*\* ready' agent-kit/ROADMAP.md || true)
if (( ready < 3 )); then echo "ROADMAP.md has $ready ready items; need >= 3"; exit 1; fi
grep -qE '^## North star' agent-kit/ROADMAP.md
echo "ok: no placeholders; $ready ready roadmap items"
