# Example: Training set cleanup

## Story

You scraped or exported 2M instruction rows. Some are garbled, mislabeled, or ambiguous. You want **`curated.jsonl`** safe to feed into fine-tuning or into **jev-triage**, without paying an LLM per row.

## Goal

Drop rows that fail **all** required gates in `rubric.yaml`. Keep audit for every rejection.

## Run (live Jev)

```bash
export TYPESAFE_API_KEY="sk-..."
jev-curate run \
  --rubric examples/training-cleanup/rubric.yaml \
  --input examples/training-cleanup/corpus.jsonl \
  --output .output/training-cleanup
```

## Run (mock — tests only)

```bash
jev-curate run --mock \
  --rubric examples/training-cleanup/rubric.yaml \
  --input examples/training-cleanup/corpus.jsonl \
  --output .output/training-cleanup-mock
```

## Next step

```bash
jev-triage run --input .output/training-cleanup/curated.jsonl ...
```

Only after curation should you spend teacher/human budget on what remains.

## Success

[SUCCESS.md](SUCCESS.md)
