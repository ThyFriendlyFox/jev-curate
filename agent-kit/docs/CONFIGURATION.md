# Configuration

jev-curate has no config file. It reads 3 sources, in this order of precedence:

| Source | Where | Wins over |
|---|---|---|
| CLI flags | the command line | everything |
| Rubric YAML | the file passed to `--rubric` | environment |
| Environment | `TYPESAFE_*` variables read by `typesafe-sdk`; `AI_GATEWAY_API_KEY` | defaults |

A rubric that does not parse stops the command with the YAML error. A rubric with no gates stops with "Rubric must define at least one gate". Neither writes output.

## CLI flags

### `jev-curate run`

| Field | Type | Default | Use |
|---|---|---|---|
| `--rubric` | path | required | Rubric YAML |
| `--input` | path | required | Input JSONL, one row per line |
| `--output` | path | required | Output dir; created if missing; re-runs resume from it |
| `--mock` | flag | off | Use the mock client. Tests only. Without it, a live key is required |
| `--gateway` | flag | off | Call live Jev through Vercel AI Gateway. Needs `AI_GATEWAY_API_KEY` in place of `TYPESAFE_API_KEY`. Not valid with `--mock` |
| `--limit` | int | none | Evaluate at most N rows this run. Skipped rows do not count |
| `--concurrency` | int ≥ 1 | `1` | Parallel Jev calls. One thread writes the files |
| `--batch-size` | int ≥ 1 | `1` | Rows per Jev call. Every gate is asked once per row in the same request. A failed call writes 1 error line per row in it. Size it by tokens: see `CLIENTS.md`, gateway |
| `--timeout` | seconds > 0 | SDK default, `10` | Wait this long for 1 Jev call. Raise it for large batches |
| `--retry-errors` | flag | off | Re-evaluate ids that appear only in `errors.jsonl` |

### `jev-curate stats`

| Field | Type | Default | Use |
|---|---|---|---|
| `--output` | path | required | A prior run's output dir |

### `jev-curate validate-rubric`

| Field | Type | Default | Use |
|---|---|---|---|
| `--rubric` | path | required | Rubric YAML to parse and list |

### `jev-curate check-jev`

Makes 1 live call. Needs `TYPESAFE_API_KEY`, or `AI_GATEWAY_API_KEY` with `--gateway`.

| Field | Type | Default | Use |
|---|---|---|---|
| `--gateway` | flag | off | Make the call through Vercel AI Gateway |

## Environment

| Field | Type | Default | Use |
|---|---|---|---|
| `TYPESAFE_API_KEY` | string | none | Required for live runs and `check-jev` without `--gateway` |
| `AI_GATEWAY_API_KEY` | string | none | Vercel AI Gateway key. Required with `--gateway` |
| `TYPESAFE_BASE_URL` | URL | `https://api.typesafe.ai` | API root, read by the SDK |
| `TYPESAFE_DEFAULT_MODEL` | string | `jev-latest` | SDK default model; the rubric's `model` overrides it per call |
| `TYPESAFE_LOG_LEVEL` | string | none | SDK logging level (`debug`, `info`, ...) |

## Rubric YAML

### Top level

| Field | Type | Default | Use |
|---|---|---|---|
| `name` | string | file stem | Shown in the run header |
| `state_field` | string | `text` | Row field sent as the main state. Other row fields ride along, except `id` and `meta`. A row with a `state` field sends that as is |
| `model` | string | `jev-latest` | Jev model for every call |
| `pass_mode` | `all` or `any` | `all` | `all`: every required gate must pass. `any`: 1 required gate passing keeps the row |
| `gates` | list | required | The gates. `questions` is accepted as an alias |

### Gate

| Field | Type | Default | Use |
|---|---|---|---|
| `name` | string | required | Unique gate name; the key in `_curation.gates` |
| `type` | `noul`, `choice`, `score` | required | Jev question kind |
| `instructions` | string | required | The question |
| `criteria` | map or list | none | `choice`: map of label to description. `score`: ordered list of level descriptions |
| `required` | bool | `true` | `false` logs the result in the audit and never rejects |
| `pass` | map | none | Pass rule; keys depend on `type` (below). A `noul` gate with no `pass` uses `min_yes: 0.5`, or `max_yes: 0.5` when its name contains `invalid`, `ambiguous`, `duplicate`, `garbled`, or `bad` |

### `pass` for `noul`

| Field | Type | Default | Use |
|---|---|---|---|
| `min_yes` | float | none | Pass when the yes probability is at least this |
| `max_yes` | float | none | Pass when the yes probability is at most this |

### `pass` for `choice`

| Field | Type | Default | Use |
|---|---|---|---|
| `allowed` | list | none | Pass only when Jev's choice is in this list |
| `min_confidence` | float | none | Pass only when the winning probability is at least this |
| `match_field` | string | none | Pass only when Jev's choice equals `row[field]`. A row without the field passes this check |

### `pass` for `score`

| Field | Type | Default | Use |
|---|---|---|---|
| `min_score` | float | none | Pass when the expected score is at least this |
| `max_score` | float | none | Pass when the expected score is at most this |
| `min_confidence` | float | none | Pass when the confidence is at least this |

<!-- Rules for this table:
     · Every shipped option appears here — an undocumented option is a
       defect. Gate `verify/gates/50_docs_cover_options.sh` checks it.
     · New options land in this table in the same PR that adds them.
     · Defaults shown here are the real defaults in code, not intended
       ones. -->
