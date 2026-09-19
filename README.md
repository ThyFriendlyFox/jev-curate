# jev-curate

Filter training JSONL with [TypeSafe Jev](https://typesafe.ai): **pass/fail gates** on every row, **`curated.jsonl`** for what survives, **`rejected.jsonl`** with a full audit trail. **Live Jev by default** — mock is test-only.

| | |
|---|---|
| **Repo purpose** | Corpus-scale **quality filter** before labeling or training (pattern #1: data curation) |
| **Sibling** | [jev-triage](https://github.com/ThyFriendlyFox/jev-triage) — route survivors to accept / teacher / human |
| **Deep dive** | [GOALS.md](GOALS.md) — success checklist, anti-goals, mock vs live |
| **Both repos** | [jev-triage docs/STACK.md](https://github.com/ThyFriendlyFox/jev-triage/blob/main/docs/STACK.md) |

---

## What problem this solves

Bad rows poison fine-tunes: hallucinated ASR, wrong buckets, ambiguous classes, labels that do not match text. LLM judges on every row are too expensive. Jev runs **cheap parallel gates** (~$21 per million 500-token examples) so you can filter the **entire** corpus, not a sample.

**Jev is not ground truth.** Curation means “good enough to enter the pipeline.” Final labels still come from humans, teachers, or **real outcomes** (pass/fail, cost, etc.).

---

## What success looks like (short)

Full checklist: [GOALS.md](GOALS.md).

> You ran **live** Jev with gates tied to real failure modes, split input into curated vs rejected with audits, **spot-checked** both sides, trained or triaged **only from `curated.jsonl`**, and measured models on **human- or outcome-labeled** eval data — not on “Jev said keep.”

---

## Quick start

```bash
pip install -e ".[dev]"
export TYPESAFE_API_KEY="sk-..."   # required for production

jev-curate check-jev

jev-curate run \
  --rubric examples/training-cleanup/rubric.yaml \
  --input examples/training-cleanup/corpus.jsonl \
  --output .output/training-cleanup
```

| Mode | Command |
|------|---------|
| **Live** | `TYPESAFE_API_KEY` set, no `--mock` |
| **Mock (tests only)** | `--mock` — CI / pytest; **not** for dataset decisions |

Without an API key the CLI **errors** — it will not silently mock production runs.

---

## Examples

| Scenario | Folder | Read |
|----------|--------|------|
| General training cleanup | [training-cleanup](examples/training-cleanup/) | [SUCCESS.md](examples/training-cleanup/SUCCESS.md) |
| Post-Whisper ASR poison | [asr-gates](examples/asr-gates/) | [SUCCESS.md](examples/asr-gates/SUCCESS.md) |
| Strict held-out eval pool | [eval-set-hygiene](examples/eval-set-hygiene/) | [SUCCESS.md](examples/eval-set-hygiene/SUCCESS.md) |

Index: [examples/README.md](examples/README.md)

Top-level `examples/rubric.yaml` and `examples/corpus.jsonl` duplicate **training-cleanup** for backward compatibility.

---

## Outputs

| File | Use |
|------|-----|
| **`curated.jsonl`** | **Input to training or jev-triage** |
| `rejected.jsonl` | Tune thresholds; sample false rejects |
| `audit.jsonl` | Every gate result per id |
| `errors.jsonl` | API failures; re-run resumes |

Each curated row includes `_curation` with failed gate names and Jev probabilities.

---

## Gates (rubric)

```yaml
pass_mode: all   # every required gate must pass

gates:
  - name: is_ambiguous
    type: noul
    instructions: Could this belong to more than one category?
    pass:
      max_yes: 0.40    # require "no" (low yes probability)

  - name: bucket_matches_content
    type: choice
    instructions: Best category from text alone
    criteria:
      billing: ...
      technical: ...
    pass:
      match_field: label
      min_confidence: 0.55
```

`required: false` logs a gate in audit without rejecting.

---

## Pipeline placement

```
Raw JSONL
  → jev-curate (this repo)     curated.jsonl | rejected.jsonl
  → jev-triage (optional)      labeling budget
  → train                      real outcome labels
```

---

## Mock vs live

| | Live | `--mock` |
|---|------|----------|
| Validates rubric semantics | Yes (spot-check humans) | No |
| Validates CLI/resume | Yes | Yes |
| OK for production manifest | Yes | **Never** |

---

## Development

```bash
pytest
jev-curate validate-rubric --rubric examples/training-cleanup/rubric.yaml
```

## License

MIT
