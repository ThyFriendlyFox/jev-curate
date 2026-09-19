#!/usr/bin/env bash
# Gate: live Jev connectivity (README "check-jev"). Needs TYPESAFE_API_KEY.
# Skips loudly without a key; never passes silently.
set -euo pipefail
cd "$(dirname "$0")/../.."
if [[ -z "${TYPESAFE_API_KEY:-}" ]]; then
  echo "SKIP: TYPESAFE_API_KEY is not set; live Jev check not run."
  exit 0
fi
jev-curate check-jev
