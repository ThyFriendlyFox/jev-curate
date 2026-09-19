#!/usr/bin/env bash
# One command answers "is this repo healthy". See agent-kit/VERIFICATION.md.
# Runs, in order: lint, build, tests, then each gate in verify/gates/.
# CI runs this same script. A gate that cannot run here skips loudly and
# never passes silently.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ -z "${VIRTUAL_ENV:-}" && -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

for tool in ruff pytest; do
  command -v "$tool" >/dev/null || { echo "verify: '$tool' not found. Run: pip install -e '.[dev]'"; exit 2; }
done
python -c "import build" 2>/dev/null || { echo "verify: 'build' not found. Run: pip install -e '.[dev]'"; exit 2; }

step() { echo; echo "== $1"; }

step "lint"
ruff check src tests
ruff format --check src tests

step "build"
rm -rf dist
python -m build --wheel --outdir dist >/dev/null
ls dist/*.whl

step "tests"
pytest -q

for gate in verify/gates/*.sh; do
  step "gate: $(basename "$gate" .sh)"
  bash "$gate"
done

echo
echo "verify: green"
