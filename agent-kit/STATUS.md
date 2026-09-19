# STATUS.md — where the project actually stands

The single source of truth for project state. Claims require evidence: a
passing gate, a linked run, a tag. Updated in the same commit as the
behavior change. The weekly cycle (WEEKLY.md step 5) refreshes it.

| Area | State | Evidence |
|---|---|---|
| Install + CLI (`run`, `stats`, `validate-rubric`, `check-jev`) | ✅ | `./verify/verify.sh` build step, gate `10_rubric`, `tests/test_cli.py` |
| Rubric gates (`noul`, `choice`, `score`, pass rules, `pass_mode`, `required`) | ✅ | `tests/test_gates.py` (7 tests) |
| Pipeline outputs (4 files, `_curation` audit) | ✅ | gate `20_mock_run` |
| Resume by id, `--limit`, `--retry-errors` | ✅ | `tests/test_pipeline.py` |
| Concurrency (`--concurrency N`) | ✅ | `test_pipeline_concurrency_matches_sequential` |
| Fail fast on bad key | ✅ | `test_auth_error_fails_fast` |
| Live Jev call | 🚧 | gate `30_live_jev` skips without `TYPESAFE_API_KEY`. Not exercised in this environment. |
| CI (`.github/workflows/ci.yml` runs `./verify/verify.sh`) | 🚧 | Workflow committed 2026-09-19; first run pending on push |
| Release | ❌ | No tag yet. Version is 0.1.0 in `pyproject.toml`. |
| Agent kit installed | ✅ | gate `40_agent_kit` |

States: ✅ done (gated) · 🚧 in progress · ❌ not started · 🧊 frozen/won't do.

## Current week

- **Shipping:** between cycles. Week of 2026-09-19 shipped "Make the README true" (see ROADMAP.md Shipped).
- **Last release:** none — 0.1.0 is unreleased.
- **Known red:** none. `./verify/verify.sh` green on 2026-09-19 (lint, build, 18 tests, 5 gates; `30_live_jev` skipped: no key).
