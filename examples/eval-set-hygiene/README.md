# Example: Eval set hygiene

## Story

You need a **small, trusted held-out set** for calibration (ECE) and accuracy. Eval contamination and ambiguous items destroy metrics. Use **stricter gates** than training cleanup.

## Goal

Reject anything ambiguous or low-confidence bucket match — prefer **precision over recall** for eval.

## Run

```bash
export TYPESAFE_API_KEY="sk-..."
jev-curate run \
  --rubric examples/eval-set-hygiene/rubric.yaml \
  --input examples/eval-set-hygiene/corpus.jsonl \
  --output .output/eval-hygiene
```

## Success

[SUCCESS.md](SUCCESS.md)
