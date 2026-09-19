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
| Live Jev call, direct (`TYPESAFE_API_KEY`) | 🚧 | gate `30_live_jev` runs it when the key is set. Not exercised: no TypeSafe key in this environment. |
| Live Jev call, Vercel AI Gateway (`--gateway`) | ✅ | `tests/test_gateway_client.py`; gate `30_live_jev` green with `AI_GATEWAY_API_KEY` on 2026-09-19 (`ok.noul=0.990`) |
| Full live run of `examples/corpus.jsonl` | 🚧 | 4 of 10 rows evaluated live on 2026-09-19. The gateway free tier returned 429 for the other 6. They wait in `errors.jsonl` for `--retry-errors`. |
| CI (`.github/workflows/ci.yml` runs `./verify/verify.sh`) | 🚧 | Workflow committed 2026-09-19; first run pending on push |
| Release | ❌ | No tag yet. Version is 0.1.0 in `pyproject.toml`. |
| Agent kit installed | ✅ | gate `40_agent_kit` |

States: ✅ done (gated) · 🚧 in progress · ❌ not started · 🧊 frozen/won't do.

## Current week

- **Shipping:** between cycles. Week of 2026-09-19 shipped "Make the README true" and the Vercel AI Gateway client (see ROADMAP.md Shipped).
- **Last release:** none — 0.1.0 is unreleased.
- **Known red:** none. `./verify/verify.sh` green on 2026-09-19 (lint, build, 30 tests, 5 gates; `30_live_jev` skipped: gateway HTTP 429).
- **Known limit:** the Vercel AI Gateway free tier allows about 4 Jev requests, then answers 429 for 10 minutes or more. It sends no `Retry-After` header.
