#!/usr/bin/env bash
# Gate: live Jev connectivity (README "check-jev"). Runs once per key that is
# set: TYPESAFE_API_KEY (direct) and AI_GATEWAY_API_KEY (Vercel AI Gateway).
# Skips loudly without a key; never passes silently.
set -euo pipefail
cd "$(dirname "$0")/../.."
ran=0
if [[ -n "${TYPESAFE_API_KEY:-}" ]]; then
  jev-curate check-jev; ran=1
fi
if [[ -n "${AI_GATEWAY_API_KEY:-}" ]]; then
  ran=1
  # The gateway free tier answers 429 for minutes at a time. That is the
  # account's quota, not a defect here, so it skips loudly instead of failing.
  if ! out="$(jev-curate check-jev --gateway 2>&1)"; then
    echo "$out"
    grep -q "(HTTP 429)" <<<"$out" || exit 1
    echo "SKIP: Vercel AI Gateway rate-limited this key (HTTP 429); live gateway check not proven this run."
  else
    echo "$out"
  fi
fi
if (( ran == 0 )); then
  echo "SKIP: neither TYPESAFE_API_KEY nor AI_GATEWAY_API_KEY is set; live Jev check not run."
fi
