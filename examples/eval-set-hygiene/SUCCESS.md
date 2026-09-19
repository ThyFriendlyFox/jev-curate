# Success criteria — eval set hygiene

## Live Jev

1. **Keep rate lower** than training-cleanup on the same corpus (stricter thresholds) — that is intentional.
2. Every row in **`curated.jsonl`** has `bucket_matches_content` pass with **`min_confidence: 0.70`** (this rubric).
3. Remaining rows get **human confirmation** on a 100% pass (eval sets are small) — Jev is pre-filter, not final arbiter.
4. You report metrics with: **“Eval set: human-adjudicated after jev-curate eval-set-hygiene”**.

## Failure signals

- Using training-cleanup thresholds for eval → ambiguous items inflate or deflate ECE.
- Skipping human pass on eval curated rows → cannot claim clean benchmark.
