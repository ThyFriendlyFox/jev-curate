# ROADMAP.md — the source of all work

**This file is not optional.** Every feature the agent builds flows down
from here. If it isn't on this roadmap, it doesn't get built; if it needs
building, it gets added here first. One item ships per weekly cycle
(see `WEEKLY.md`).

## North star

jev-curate is the cheap first pass over a training corpus: every row goes
through pass/fail gates answered by TypeSafe Jev, what passes is kept,
what fails is rejected with a written reason, and a re-run never pays
twice. It stays a filter. It never becomes the teacher of record: no Jev
answer turns into a training label. It scales by concurrency and by
sharding, and it hands its output to `jev-triage` for the expensive
labeling budget.

## Feature Queue — ordered; top unblocked item ships next

<!-- RULES:
     · Always ≥3 ready items. Refilling the queue is part of every weekly
       cycle (WEEKLY.md step 7) — a starving queue is a failed cycle.
     · Order is priority. The agent takes the TOP unblocked item and may
       not reorder without recording why (below, under "Queue changes").
     · Every item carries a completion promise: ONE testable sentence
       that is unambiguously true or false. No promise, not ready.
     · "Evidence" names how the promise will be proven: which gate,
       screenshot, benchmark, or user-visible behavior. -->

provisional: true — the human has not ranked these yet.

### 1. `jev-curate merge`
- **Promise:** `jev-curate merge --output <dir> <run1> <run2> ...` writes one `curated.jsonl` and one `rejected.jsonl` in which each id appears once, and reports how many duplicates it dropped.
- **Evidence:** `tests/test_merge.py` merges 2 mock runs with 1 overlapping id; gate `20_mock_run` extended to shard, run twice, merge, and count.
- **Use case:** docs/USE-CASES.md "Shard and merge".
- **Scope guard:** No re-evaluation, no conflict resolution beyond first-seen wins, no `audit.jsonl` merging.
- **Status:** ready

### 2. Token and cost report
- **Promise:** After a run, `jev-curate stats --output <dir>` prints total `input_tokens` from Jev usage and an estimated cost at a `--rate` per million tokens (default 0.042 USD).
- **Evidence:** `audit.jsonl` rows carry `usage`; `tests/test_cli.py::test_stats_reports_tokens` with the mock's word-count usage; row for `--rate` in docs/CONFIGURATION.md.
- **Use case:** docs/USE-CASES.md "Estimate cost before a full run".
- **Scope guard:** No live pricing lookup; no per-gate cost split.
- **Status:** ready

### 3. Retry policy for large runs
- **Promise:** `run --max-retries N` and `--retry-timeout S` build `LiveJevClient` with a `RetryPolicy(max_retries=N, timeout=S)`, and a unit test proves the policy reaches the SDK client.
- **Evidence:** `tests/test_client.py` inspects the constructed `TypeSafeClient` retry policy; rows in docs/CONFIGURATION.md.
- **Use case:** docs/USE-CASES.md "Curate at scale".
- **Scope guard:** No custom backoff; the SDK's `RetryPolicy` is the whole surface.
- **Status:** ready

### 4. Review sample
- **Promise:** `jev-curate sample --output <dir> --n 50` writes `sample.jsonl` with 50 random rejected rows and their failed gates for a human spot check.
- **Evidence:** `tests/test_cli.py::test_sample`; docs row for `--n`.
- **Use case:** docs/USE-CASES.md "Spot-check what was dropped".
- **Scope guard:** No UI, no labeling, no writing back.
- **Status:** ready

### 5. Calibrate the example rubric against live Jev
- **Promise:** On `examples/corpus.jsonl` with live Jev, the example rubric keeps every row the corpus marks clean and rejects every row it marks bad, and `examples/live-run.md` records the live probabilities behind each threshold.
- **Evidence:** A committed `examples/live-run.md` table of per-gate live probabilities; gate `20_mock_run` still green; the mock's heuristics updated only if the gate names change.
- **Use case:** docs/USE-CASES.md "Filter a labeled corpus".
- **Scope guard:** No new gate kinds. Reword or re-threshold `duplicate_substance` and `is_ambiguous` only. Jev sees 1 row per call, so a gate must not ask about other rows.
- **Status:** ready

### 6. Pace requests
- **Promise:** `run --min-interval S` starts each Jev call at least S seconds after the last one, and a test proves it with a fake clock.
- **Evidence:** `tests/test_pipeline.py::test_min_interval_spaces_calls`; row for `--min-interval` in docs/CONFIGURATION.md; the TREC demo runs as 1 command.
- **Use case:** docs/USE-CASES.md "Batch rows under a request quota".
- **Scope guard:** A fixed interval only. No adaptive backoff, no reading of rate-limit headers (the gateway sends none).
- **Status:** ready

## Later — candidates, not yet specced

- Async client (`AsyncTypeSafeClient`) — higher throughput than threads once rate limits allow it.
- Local exact-duplicate pass before Jev — hash the state field; skip a paid call for byte-identical rows.
- HTML audit report — one page per run: keep rate, reject gates, sample rows.
- Per-gate skip on resume — re-run only new gates when a rubric grows.

## Shipped

| Week | Feature | Release | Evidence |
|---|---|---|---|
| 2026-09-19 | Batch rows per request: `run --batch-size N` asks every gate once per row in 1 Jev call; `--timeout S` | unreleased | `test_pipeline_batches_match_unbatched`, `test_batch_is_one_call_with_every_gate_per_row`; live: 75 rows, 150 answers, 1 request, 0.9 s; `ralph/GOAL.md` line 18 |
| 2026-09-19 | Vercel AI Gateway client: `run --gateway` and `check-jev --gateway` reach live Jev with `AI_GATEWAY_API_KEY` | unreleased | `tests/test_gateway_client.py` (9 tests); live `check-jev --gateway` returned `ok.noul=0.990`; `ralph/GOAL.md` line 17 |
| 2026-09-19 | Make the README true: gated quick start, concurrency, `--retry-errors`, fail-closed gates, fail-fast on bad key, agent kit, Ralph loop | unreleased | `./verify/verify.sh` green on branch `claude/ralph-loop-implementation-meir2m`; `ralph/GOAL.md` checklist |

## Explicitly not doing

- Using Jev answers as training labels — the README's one rule: filter with Jev, train on real outcome labels.
- A triage queue (keep / teacher / human) — that is `jev-triage`'s job.
- A hosted service or UI — this is a CLI over JSONL.

## Queue changes

- 2026-09-19 — Added item 6 from the 1,000-row live run. The free tier needs 90 seconds between large requests and a 10-minute wait after 3. I drove that with a scratch shell loop; the tool needs the flag. Item 3 (retry policy) gained weight too: the SDK's 2 retries turn 1 refused batch into 3 requests of quota.
- 2026-09-19 — The human asked for many rows in 1 request, because the gateway free tier limits requests, not tokens. It shipped the same day, ahead of the queue. Promise: `run --batch-size N` evaluates N rows in 1 Jev call and writes the same verdicts as N calls. Use case: docs/USE-CASES.md "Batch rows under a request quota".
- 2026-09-19 — The human asked for a Vercel AI Gateway client, because their Jev access is a gateway key. It shipped the same day, ahead of the queue. Promise: `run --gateway` evaluates the rubric through live Jev on the gateway and a rejected key stops the run. Use case: docs/USE-CASES.md "Run with a Vercel AI Gateway key". The 4 ready items keep their order.
- 2026-09-19 — Added item 5 from the first full live run: `duplicate_substance` rejected clean rows (`t001` yes=0.75 against `max_yes: 0.35`). I queued it last; the human has not ranked the queue.
- 2026-09-19 — The first live run showed the gateway free tier returns 429 after about 4 requests. This raises the value of item 3 (retry policy). I did not reorder; the human has not ranked the queue.
- 2026-09-19 — Queue seeded during SETUP.md from README gaps (`merge`, cost, retry policy, sample). Provisional until the human ranks it.
