# Examples — jev-curate

Each example includes: **story**, **run command**, and **[SUCCESS.md](training-cleanup/SUCCESS.md)** defining what a good run means.

```bash
pip install -e ".[dev]"
export TYPESAFE_API_KEY="sk-..."

jev-curate check-jev   # optional

jev-curate run \
  --rubric examples/<scenario>/rubric.yaml \
  --input examples/<scenario>/corpus.jsonl \
  --output .output/<scenario>
```

Tests use `--mock` only:

```bash
jev-curate run --mock --rubric ... --input ... --output .output/test
```

---

## Example index

| Folder | Scenario | Primary gates |
|--------|----------|----------------|
| [training-cleanup](training-cleanup/) | General ML JSONL before fine-tuning | valid text, plausible label, not ambiguous, bucket match |
| [asr-gates](asr-gates/) | Post-Whisper transcripts | ASR plausible, not hallucination |
| [eval-set-hygiene](eval-set-hygiene/) | Building a clean **held-out eval** set | stricter thresholds; drop ambiguous |

---

## JSONL schema

```json
{"id": "stable-id", "text": "...", "label": "your-bucket"}
```

Jev `state` includes `text` **and** other fields (e.g. `label`) when present — required for `label_plausible` and `match_field` gates.

---

## Outputs (every example)

| File | Meaning |
|------|---------|
| `curated.jsonl` | **Train or triage from here** |
| `rejected.jsonl` | Audit why dropped; sample for threshold tuning |
| `audit.jsonl` | All gate pass/fail in one place |

Legacy top-level `examples/rubric.yaml` points at the same content as **training-cleanup**.
