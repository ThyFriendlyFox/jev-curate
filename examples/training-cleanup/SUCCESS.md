# Success criteria — training cleanup

## You succeeded when (live Jev)

1. **`t006`-class rows** (garbled / hallucinated text in the toy corpus) appear in **`rejected.jsonl`** with `failed_gates` including `transcript_valid` or similar.
2. **`t005`, `t010`-class ambiguous rows** fail `is_ambiguous` or `bucket_matches_content` — **rejected**, not curated.
3. **Clear billing/technical/sales rows** with consistent `label` appear in **`curated.jsonl`**.
4. **`audit.jsonl` line count** equals input row count (every id judged once).
5. Manual sample: **≤5% false rejects** on curated (good rows wrongly dropped) at your tolerance; if higher, loosen `pass.min_yes` / `max_yes` and re-run on a shard.
6. Training manifest states: **“Base split = jev-curate curated.jsonl run `<date>` rubric `<hash>`”** — reproducibility.

## Mock mode success

- 10/10 processed, 0 errors
- `curated` + `rejected` = 10
- Re-run skips 10

Mock **does not** validate your gate wording — only plumbing.

## Failure signals

| Signal | Likely cause |
|--------|----------------|
| 95%+ curated | Gates too loose; inspect rejected.jsonl (empty) |
| 95%+ rejected | Gates too strict or wrong `match_field` |
| `bucket_matches_content` false positives | Label schema ≠ Choice criteria keys |
| Training without reviewing rejected sample | Process failure |

## What this example does *not* prove

- Cross-row duplicate removal (use MinHash/embeddings separately).
- Correctness of `label` as **ground truth** — only plausibility vs text.
