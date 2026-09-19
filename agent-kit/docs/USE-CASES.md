# Use cases

Each case has the same shape.
**Prepare** names the rubric and input. **Run** is the command. **Use** is what the output is for.

## Filter a labeled corpus

**Prepare.** Write a rubric with 1 gate per thing you do not want to train on: garbled text, wrong label, ambiguity.
**Run.** `jev-curate run --rubric rubric.yaml --input corpus.jsonl --output out/`.
**Use.** Train on `out/curated.jsonl`. Keep `out/rejected.jsonl` as the record of what was dropped and why.

## Check a label column against content

**Prepare.** Add a `choice` gate whose `criteria` are your labels and whose `pass` has `match_field: label` and a `min_confidence`.
**Run.** The same `run` command.
**Use.** Rows whose content does not match their label land in `rejected.jsonl` with the gate named in `_curation.failed_gates`.

## Drop ambiguous examples

**Prepare.** Add a `noul` gate that asks "could this belong to more than one category?" with `pass: {max_yes: 0.4}`.
**Run.** The same `run` command.
**Use.** The kept set has fewer boundary cases. Lower `max_yes` to be stricter.

## Audit without dropping

**Prepare.** Set `required: false` on a gate you want to measure but not enforce.
**Run.** The same `run` command.
**Use.** Read the gate's result in `audit.jsonl` for every row. Nothing is rejected because of it.

## Resume an interrupted run

**Prepare.** Nothing. The output dir is the checkpoint.
**Run.** Re-run the same command with the same `--output`.
**Use.** Ids already in `curated`, `rejected`, or `errors` are skipped. The `Skipped (resume)` row shows how many.

## Retry API failures

**Prepare.** Check `errors.jsonl` for rows that failed on a timeout or a 5xx.
**Run.** `jev-curate run ... --retry-errors`.
**Use.** Only the errored ids are re-evaluated. Succeeding rows move to `curated` or `rejected`.

## Run with a Vercel AI Gateway key

**Prepare.** Export `AI_GATEWAY_API_KEY`. No TypeSafe key is needed.
**Run.** `jev-curate run --gateway --rubric rubric.yaml --input corpus.jsonl --output out/`.
**Use.** The same live Jev answers the gates, billed to the Vercel account. On the free tier, rate-limited rows land in `errors.jsonl`; run again later with `--retry-errors`.

## Curate at scale

**Prepare.** Know your TypeSafe rate limit.
**Run.** `jev-curate run ... --concurrency 8`.
**Use.** 8 Jev calls run at once; the files are still written in order by 1 thread. Raise the number until the API starts returning 429s, then back off.

## Shard and merge

**Prepare.** Split the input JSONL into N files.
**Run.** Run N workers, each with its own `--output` dir.
**Use.** Merge the `curated.jsonl` files downstream. A `jev-curate merge` command is queued in ROADMAP.md.

## Estimate cost before a full run

**Prepare.** Take a slice: `--limit 100`.
**Run.** `jev-curate run ... --limit 100`, then `jev-curate stats --output out/`.
**Use.** Multiply by the corpus size. Jev is priced per input token (0.042 USD per million at the time of writing); a token report is queued in ROADMAP.md.

## Curate, then triage

**Prepare.** Finish a curation run.
**Run.** Point `jev-triage` at `out/curated.jsonl`.
**Use.** Cheap gates first, expensive labeling budget only on what passed. Jev filters; it never becomes the teacher of record.
