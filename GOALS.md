# Goals — jev-curate

## What this repo is for

**jev-curate** is a batch pipeline that uses [TypeSafe Jev](https://typesafe.ai) to **keep or drop** training examples before you spend money on labeling or GPU time. Every row passes a YAML-defined set of **gates** (Noul / Choice / Score + pass rules). Failures go to `rejected.jsonl` with an audit trail; passes go to `curated.jsonl`.

It is **not** a triage router (see [jev-triage](https://github.com/ThyFriendlyFox/jev-triage)), **not** a trainer, and **not** a source of ground-truth labels. It is a **quality filter** at corpus scale.

## Primary goals

1. **Filter the whole corpus** — Not a random sample: every `id` gets the same gates (~$21 per million 500-token rows at Jev pricing).
2. **Make drops explainable** — Each rejection records **which gate failed** and Jev’s probabilities in `_curation` / `audit.jsonl`.
3. **Use live Jev in production** — `typesafe-sdk` → `jev-latest`; mock is for tests only (`--mock`).
4. **Protect training from poison** — Garbled ASR, implausible labels, ambiguous multi-class rows, and content/label mismatch are dropped *before* triage or training.
5. **Stay resumable** — Crash-safe JSONL append; re-run skips finished ids.

## What success looks like

You have used **jev-curate successfully** when all of the following are true:

| # | Success criterion | How you verify |
|---|-------------------|----------------|
| 1 | Gates match **failure modes you’ve seen in production** (bad ASR, wrong bucket, duplicates) | Rubric review + [examples/](examples/) |
| 2 | Production run used **`TYPESAFE_API_KEY`** (no `--mock`) | Logs / CLI banner says `live` |
| 3 | **`curated.jsonl` + `rejected.jsonl`** partition your input ids without gaps (plus `errors.jsonl` if any) | Count ids vs input |
| 4 | You **spot-checked** rejected rows (e.g. 50–100) — mostly true positives, not good data lost | Manual review |
| 5 | You **spot-checked** curated rows — failure rate acceptable for your risk tolerance | Manual review |
| 6 | Downstream training or **jev-triage** runs **only on `curated.jsonl`** (or a manifest derived from it) | Pipeline docs |
| 7 | **Training targets** still come from real outcomes / human labels — curation is not “the label” | Dataset spec |
| 8 | Re-run after interrupt shows **`Skipped (resume)`** without duplicate ids | Second run |

### Anti-goals (not success)

- Training exclusively on rows because they “passed Jev” with no human/outcome evaluation.
- Using `--mock` to decide what ships to production.
- Expecting one gate to fix **duplicate detection across rows** (this tool is **per-row**; dedup needs embeddings or hash clustering elsewhere).
- Using Jev on audio **without** text in `state` (transcribe or caption first).

## Typical placement

```
Raw JSONL
  → jev-curate (this repo)     curated.jsonl | rejected.jsonl
  → jev-triage (optional)      accept | teacher | human
  → expensive labeling
  → train on real outcome labels
```

## Mock vs live

| Mode | Purpose |
|------|---------|
| **Live** (default when `TYPESAFE_API_KEY` set) | Real curation decisions |
| **`--mock`** | Unit tests and CI only |

CLI **refuses** to run live without a key; it does not silently mock in production.

See [examples/README.md](examples/README.md).
