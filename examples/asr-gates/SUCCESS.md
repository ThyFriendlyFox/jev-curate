# Success criteria — ASR gates

## Live Jev

1. Hallucination-like rows (music tokens, repeated “the the”) → **`rejected.jsonl`**, gate `asr_plausible`.
2. Short but valid utterances → **curated** unless `has_semantic_content` fails.
3. You manually listened to **≥20 rejected** clips — majority are true ASR failures.
4. Downstream lexical labeling (Jev triage or humans) runs **only on `curated.jsonl`**.

## Does not validate

- Speaker emotion, noise floor, overlap (acoustic) — needs separate labels.
- Whisper quality on full 8k-hour corpus — this only gates text.

## Mock

Heuristic on `garbled`, `music`, `hallucin` substrings — use for CI only.
