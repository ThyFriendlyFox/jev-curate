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
| Full live run of `examples/corpus.jsonl` | ✅ | 2026-09-19, `--gateway`: 10 of 10 rows evaluated, 2 kept, 8 rejected. It took 3 `--retry-errors` passes with 10-minute gaps because of the free-tier 429s. |
| Batched rows (`--batch-size N`) | ✅ | `test_pipeline_batches_match_unbatched`; live on 2026-09-19: 75 rows and 150 answers in 1 request, 0.9 s |
| 1,000-row Hugging Face run (`examples/trec/`) | 🚧 | 310 of 1,000 rows on 2026-09-19: 34 of 35 flipped labels and 15 of 15 scrambled texts rejected; 23 of 260 untouched rows rejected. The run continues at 180 rows per 14 minutes, the free-tier pace. |
| Example rubric thresholds against live Jev | 🚧 | `duplicate_substance` rejected 7 of 10 rows live, 3 of them on that gate alone (`t001` yes=0.75, `t003` 0.47, `t009` 0.41). The threshold was set against the mock. Queued as ROADMAP item 5. |
| CI (`.github/workflows/ci.yml` runs `./verify/verify.sh`) | ✅ | Run 35445240451 passed on `master` at `94435b0` (2026-09-19) |
| Release | ❌ | No tag yet. Version is 0.1.0 in `pyproject.toml`. |
| Agent kit installed | ✅ | gate `40_agent_kit` |

States: ✅ done (gated) · 🚧 in progress · ❌ not started · 🧊 frozen/won't do.

## Current week

- **Shipping:** between cycles. Week of 2026-09-19 shipped "Make the README true" and the Vercel AI Gateway client (see ROADMAP.md Shipped).
- **Last release:** none — 0.1.0 is unreleased.
- **Known red:** none. `./verify/verify.sh` green on 2026-09-19 (lint, build, 36 tests, 5 gates; `30_live_jev` skipped: gateway HTTP 429). `check-jev --gateway` passed by hand at 09:22 on the merged code.
- **Known limit:** the Vercel AI Gateway free tier passes about 3 large or 4 small Jev requests, then answers 429 until about 10 quiet minutes pass. Requests of 100 rows or more always got 503; smaller ones sometimes did. The cause is not proven. `docs/CLIENTS.md` lists the observations. It sends no `Retry-After` header.
