#!/usr/bin/env bash
# Gate: every CLI flag and every rubric key is documented in
# agent-kit/docs/CONFIGURATION.md (an undocumented option is a defect).
set -euo pipefail
cd "$(dirname "$0")/../.."
doc=agent-kit/docs/CONFIGURATION.md
missing=0
for flag in $(grep -oE '"--[a-z-]+"' src/jev_curate/cli.py | tr -d '"' | sort -u); do
  grep -q -- "\`$flag" "$doc" || { echo "undocumented CLI flag: $flag"; missing=1; }
done
for key in name state_field model pass_mode gates type instructions criteria required pass \
           min_yes max_yes allowed min_confidence match_field min_score max_score; do
  grep -q "\`$key\`" "$doc" || { echo "undocumented rubric key: $key"; missing=1; }
done
exit $missing
