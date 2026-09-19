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

On the gateway free tier, send 1 request of 60 rows every 200 seconds. Add
`--limit 60 --retry-errors` to send 1 request for each command. That pace
passed 11 times in a row. Bursts did not: see `agent-kit/docs/CLIENTS.md`,
gateway.

## Result

All 1,000 rows, live Jev through the gateway, 2026-09-19. 19 requests carried
the 1,000 rows and 2,000 answers. Jev kept 773 rows and rejected 227.

| Rows | Rejected |
|---|---|
| Label flipped | 99 of 100. For 91 of them Jev chose the original label |
| Text scrambled | 50 of 50 |
| Not touched | 78 of 850 (9%) |

The 1 flipped row that Jev kept is "What is the `` 7-minute cigarette '' ?".
The source label is DESC, the flip made it ENTY, and Jev also chose ENTY.

8 rows that were not touched failed `well_formed`. They are real faults in the
source data. 5 contain part-of-speech tags from the original TREC files:

- `trec-79`: "What country did the Nazis occupy for 1 , CD NNS IN NNP NNP NNP ."
- `trec-246`: "Who wrote NN DT NNP NNP '' ?"
- `trec-253`: "What schools in the Washington , DC NN NN VBP NN NN NN NN ."

3 have lost characters, such as `trec-462`: "What country did King Gustav V
reign over from 197 to 195 ?".

The other 70 are label disagreements. Jev was at 0.9 or above on 14 of them,
such as "Where do chihuahuas come from ?" (label DESC, Jev LOC at 0.98). It
was under 0.6 on 21. The rubric has no confidence threshold and was not tuned
on this data; a threshold would keep most of the 21.

Cost: 1 request of 75 rows and 150 questions used 15,609 input tokens and
returned in 0.9 seconds. The shared state is counted once. Each question adds
about 100 tokens.
