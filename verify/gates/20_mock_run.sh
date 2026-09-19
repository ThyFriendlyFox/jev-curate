#!/usr/bin/env bash
# Gate: the README quick start works end to end in mock mode and produces
# the 4 documented output files with consistent counts; a re-run resumes.
set -euo pipefail
cd "$(dirname "$0")/../.."
out="$(mktemp -d)"
trap 'rm -rf "$out"' EXIT

jev-curate run --mock --rubric examples/rubric.yaml --input examples/corpus.jsonl --output "$out" >"$out/run1.log"
cat "$out/run1.log"

python - "$out" <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
def rows(name):
    p = out / f"{name}.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
curated, rejected, audit, errors = rows("curated"), rows("rejected"), rows("audit"), rows("errors")
n_in = sum(1 for l in (Path("examples/corpus.jsonl").read_text().splitlines()) if l.strip())
assert errors == [], f"mock run produced errors: {errors}"
assert len(curated) + len(rejected) == n_in, (len(curated), len(rejected), n_in)
assert len(audit) == n_in, len(audit)
assert all(r["_curation"]["kept"] is True for r in curated)
assert all(r["_curation"]["kept"] is False and r["_curation"]["failed_gates"] for r in rejected)
assert all(set(a["gates"]) == {"transcript_valid","label_plausible","is_ambiguous","duplicate_substance","bucket_matches_content"} for a in audit)
assert curated, "expected at least one kept example"
assert rejected, "expected at least one rejected example"
print(f"ok: {len(curated)} curated, {len(rejected)} rejected, {len(audit)} audited")
PY

# Resume: second run over the same output dir skips every id.
jev-curate run --mock --rubric examples/rubric.yaml --input examples/corpus.jsonl --output "$out" >"$out/run2.log"
grep -E "Skipped \(resume\).*10" "$out/run2.log" >/dev/null || { cat "$out/run2.log"; echo "resume did not skip all rows"; exit 1; }
echo "ok: resume skipped all rows"

jev-curate stats --output "$out" >/dev/null
echo "ok: stats"
