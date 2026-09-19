# GOAL.md — what success looks like

The loop's target. Derived from `README.md`, which defines the product.
The loop ends when every line below is true and `./verify/verify.sh` is
green. Each line names the gate that proves it. A line with no gate is
proven by hand and says so.

## The promise

`jev-curate` filters a JSONL corpus with TypeSafe Jev pass/fail gates,
keeps what passes, drops the rest, and leaves an audit trail. Live Jev
is the default; mock exists for tests only.

## Checklist

| # | Success looks like | Proof |
|---|---|---|
| 1 | `pip install -e ".[dev]"` installs the package and the `jev-curate` command | `verify.sh` build step + gate `10_rubric` |
| 2 | `pytest` passes | `verify.sh` tests step |
| 3 | `jev-curate validate-rubric --rubric examples/rubric.yaml` lists every gate | gate `10_rubric` |
| 4 | `jev-curate run` writes `curated.jsonl`, `rejected.jsonl`, `audit.jsonl`, `errors.jsonl` as the README table describes | gate `20_mock_run` |
| 5 | A kept row passed every required gate; a rejected row names the failed gates in `_curation` | gate `20_mock_run` |
| 6 | A re-run over the same output dir skips ids already in the 3 result files | gate `20_mock_run` |
| 7 | `jev-curate stats --output <dir>` summarizes a prior run | gate `20_mock_run` |
| 8 | `jev-curate check-jev` makes one live call when `TYPESAFE_API_KEY` is set, and `check-jev --gateway` when `AI_GATEWAY_API_KEY` is set | gate `30_live_jev` (skips loudly without a key) |
| 9 | Live is the default; `run` without a key fails with a plain message | test `test_run_without_key_fails` |
| 10 | Rubric gates support `noul`, `choice`, `score` with the documented pass rules, `pass_mode`, and `required: false` | tests in `tests/test_gates.py` |
| 11 | A gate Jev did not answer fails closed (required → reject) | test `test_missing_answer_fails_required_gate` |
| 12 | Concurrent `system_one` calls are a real option, not "reserved" | test `test_pipeline_concurrency_matches_sequential`, `--concurrency` documented |
| 13 | A bad API key stops the run at once instead of writing N error rows | test `test_auth_error_fails_fast` |
| 14 | The agent kit is installed with no placeholders and a ready roadmap | gate `40_agent_kit` |
| 15 | Every CLI flag and rubric key is documented | gate `50_docs_cover_options` |
| 16 | CI runs the same `verify.sh` as local | `.github/workflows/ci.yml` (proven by hand: the file calls the script) |
| 17 | `--gateway` reaches live Jev through Vercel AI Gateway with the same answers, confidence, and fail-fast on a bad key | tests in `tests/test_gateway_client.py`; gate `30_live_jev` with `AI_GATEWAY_API_KEY` |

## Out of scope for this loop

- Cutting a release tag (RELEASING.md; the human decides).
- Async client (`AsyncTypeSafeClient`); thread concurrency is enough for now.
- Anything not traceable to `README.md` or `agent-kit/ROADMAP.md`.
