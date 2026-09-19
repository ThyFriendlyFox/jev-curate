# Example: ASR / transcript gates

## Story

Whisper produced transcripts for a speech dataset. Before any labeling budget, you must **remove ASR poison** (hallucinations on silence/music) so bad text never becomes training signal.

## Goal

Single-purpose rubric: **`asr_plausible`** and **`has_semantic_content`**. Stricter than general cleanup.

## Run

```bash
export TYPESAFE_API_KEY="sk-..."
jev-curate run \
  --rubric examples/asr-gates/rubric.yaml \
  --input examples/asr-gates/corpus.jsonl \
  --output .output/asr-gates
```

## Success

[SUCCESS.md](SUCCESS.md)
