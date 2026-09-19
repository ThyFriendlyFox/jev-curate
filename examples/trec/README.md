# TREC demo: clean 1,000 Hugging Face rows with batched requests

This example takes 1,000 rows of the Hugging Face set
[`SetFit/TREC-QC`](https://huggingface.co/datasets/SetFit/TREC-QC) (questions
with an answer-type label) and filters them with live Jev. It sends 60 rows in
each request.

TREC is a clean set. To measure the filter, `prepare.py` corrupts a recorded
share of the rows with a fixed seed: it flips 100 labels and scrambles 50
texts. Jev never sees the record or the label. The text is in the `state`
field, so only the text is sent.

## Run it

```bash
python examples/trec/prepare.py .output/trec
export AI_GATEWAY_API_KEY="vck_..."
jev-curate run --gateway --batch-size 60 --timeout 120 \
  --rubric examples/trec/rubric.yaml \
  --input .output/trec/corpus.jsonl --output .output/trec/run1
python examples/trec/score.py .output/trec .output/trec/run1
```

On the gateway free tier, what worked was 3 requests, 90 seconds apart, then
10 quiet minutes. A refused request can still happen; run again later. Add `--limit 60 --retry-errors` to send 1 request for each command.
See `agent-kit/docs/CLIENTS.md`, gateway, for the measured limits.

## Result

Interim: 310 of 1,000 rows on 2026-09-19. The run is in progress.

| Rows | Rejected |
|---|---|
| Label flipped | 34 of 35 (97%). For 30 of them Jev chose the original label |
| Text scrambled | 15 of 15 (100%) |
| Not touched | 23 of 260 (9%) |

Some rejected rows that were not touched are real faults in the source data.
The `well_formed` gate rejected `trec-79` ("What country did the Nazis occupy
for 1 , CD NNS IN NNP NNP") and `trec-144` ("What is the origin of the word ,
JJ ."). Both contain part-of-speech tags from the original TREC files.

Other rejected rows are label disagreements. Some are arguable: "Where do
chihuahuas come from ?" has the label DESC, and Jev chose LOC at 0.98. Some
have a confidence near 0.5. The rubric has no confidence threshold; it was not
tuned on this data.

Cost: 1 request of 75 rows and 150 questions used 15,609 input tokens and
returned in 0.9 seconds. The shared state is counted once. Each question adds
about 100 tokens.
