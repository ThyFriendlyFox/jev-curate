# Architecture

jev-curate is a Python 3.10 command-line program over JSONL files. The code has 5 parts.

| Part | Folder | Task |
|---|---|---|
| CLI | `src/jev_curate/cli.py` | Parse flags, pick live or mock, run the pipeline, print tables |
| Rubric | `src/jev_curate/rubric.py` | Load YAML into typed gates and pass rules; build Jev questions |
| Client | `src/jev_curate/client.py`, `gateway_client.py`, `mock_client.py` | The `JevClient` seam: one `evaluate` call per row. Live uses `typesafe-sdk`; gateway is live Jev through Vercel AI Gateway; mock is for tests |
| Gates | `src/jev_curate/gates.py`, `audit.py` | Turn Jev answers into pass/fail per gate and one verdict per row |
| Pipeline | `src/jev_curate/pipeline.py` | Read rows, skip done ids, call the client (optionally in threads), append the 4 output files |

## Data flow

1. The user runs `jev-curate run --rubric R --input I --output O`.
2. `cli.run` loads the rubric and refuses to go live without `TYPESAFE_API_KEY` (`AI_GATEWAY_API_KEY` with `--gateway`).
3. `CurationPipeline.run` reads ids already in `O/curated.jsonl`, `O/rejected.jsonl`, and `O/errors.jsonl` (the last one unless `--retry-errors`).
4. For each remaining row, `_extract_state` builds the state: the `state_field` text plus the row's other fields.
5. `evaluate_rubric` sends the state and every gate's question to Jev in 1 `system_one` call and gets 1 answer per gate. With `--batch-size N`, `evaluate_rubric_batch` sends N rows as 1 state (`{"rows": {"r1": ..., "r2": ...}}`) and asks each gate once per row under the name `r1__<gate>`; each question names the row it judges.
6. `evaluate_curation` applies each gate's pass rule. A missing answer fails. Required failures reject the row.
7. `_record` appends the audit line, then the row plus `_curation` to `curated.jsonl` or `rejected.jsonl`. An exception becomes a line in `errors.jsonl`.
8. `summarize` counts the 4 files and the CLI prints the result tables.

## Verify and loop

| File | Task |
|---|---|
| `verify/verify.sh` | Lint, build, tests, then every `verify/gates/*.sh` |
| `verify/gates/*.sh` | One repo gate each; see `agent-kit/VERIFICATION.md` |
| `ralph/loop.sh` | Feeds `ralph/PROMPT.md` to an agent until `verify.sh` is green |
| `.github/workflows/ci.yml` | Runs `verify.sh` on push and pull request |

## Boundaries

| Boundary | Rule |
|---|---|
| CLI ↔ Pipeline | Flags cross as `PipelineConfig` fields. The pipeline never reads the environment or prints. |
| Pipeline ↔ Client | Only `JevClient.evaluate(state, questions, model=)` crosses. The pipeline never imports `typesafe_sdk` transport code; it catches `TypeSafeAuthenticationError` and lets it propagate. |
| Client ↔ Gates | Answers cross as SDK answer objects; `audit.serialize_answer` is the only place that turns them into JSON. |
| Gates ↔ Rubric | Pass rules are dataclasses on `GateSpec`. Gate code never reads YAML. |
| Worker threads ↔ files | Workers return `_Outcome`; only the calling thread appends to the output files. |
| Row ↔ `_curation` | The pipeline adds `_curation` and changes nothing else on the row. |
