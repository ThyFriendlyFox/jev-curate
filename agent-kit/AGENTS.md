# AGENTS.md — the binding contract

In effect whenever code in this repo is touched, by agent or human.
When this conflicts with intuition, this wins.

## Commands

```sh
pip install -e ".[dev]"                                   # once per checkout
python -m build --wheel --outdir dist                     # build
pytest                                                    # tests
ruff check src tests && ruff format --check src tests     # lint / format check
./verify/verify.sh                                        # full health gate — must pass before any push
```

Requires Python 3.10.

## Invariants — never regress these

1. **Live Jev is the default.** `--mock` exists for tests only. No production
   code path imports `jev_curate.mock_client`; `make_client(live=True)` is the
   only way to reach the API.
2. **Jev filters; it does not label.** The pipeline never writes a Jev answer
   into a training field. `_curation` is the only field it adds to a row, and
   the row's own fields stay untouched.
3. **A kept row passed every required gate.** `pass_mode: all` is the default.
   A gate with no answer from Jev fails closed. `required: false` gates land in
   the audit and never reject.
4. **The output contract is 4 files.** `curated.jsonl`, `rejected.jsonl`,
   `audit.jsonl`, `errors.jsonl`, all append-only JSONL in the output dir.
   Every curated and rejected row carries `_curation`; `audit.jsonl` has one
   line per evaluated row.
5. **Resume is by id.** Ids present in `curated`, `rejected`, or `errors` are
   skipped on re-run. Only `--retry-errors` re-evaluates errored ids.
6. **Only the calling thread writes.** Worker threads call Jev and return an
   outcome; `CurationPipeline._record` appends. Records never interleave.
7. **A bad API key stops the run.** `TypeSafeAuthenticationError` propagates
   instead of becoming N error rows.
8. **The rubric YAML is the only place gate semantics live.** Pass rules are
   typed per gate kind (`noul`, `choice`, `score`). Code never hardcodes a
   threshold for a named gate, except the name-based default in
   `_default_noul_rule` for gates with no `pass:` block.
9. **Secrets enter through the environment only.** `TYPESAFE_API_KEY` is read
   from the environment; no key in code, fixtures, or docs.

## Landmine map

| Area | Why it bites |
|---|---|
| `pipeline.py::_extract_state` | Merges row metadata (like `label`) into the state so `label_plausible` gates can see it. Drop it and label gates silently judge without the label. |
| `gates.py::_default_noul_rule` | A gate with no `pass:` block gets its direction from its name (`ambiguous`, `duplicate`, `bad` → `max_yes`). Renaming a gate flips its default. Always write a `pass:` block. |
| `pipeline.py::load_done_ids` | `errors.jsonl` counts as done. A transient API failure is never retried unless the user passes `--retry-errors`. |
| `mock_client.py` | Regex heuristics tuned to `examples/corpus.jsonl`. Editing the corpus changes what gate `20_mock_run` sees. Mock probabilities mean nothing outside tests. |
| `cli.py --limit` | Counts rows evaluated this run, not lines read. Skipped rows do not count. |
| `verify/gates/50_docs_cover_options.sh` | A new CLI flag or rubric key with no row in `docs/CONFIGURATION.md` turns verify red. Add the row in the same commit. |
| `verify/gates/40_agent_kit.sh` | Fewer than 3 `**Status:** ready` items in `ROADMAP.md` turns verify red. Refill the queue when you take an item. |

## House style

- Match the surrounding code's idiom, naming, and comment density.
- No demo scaffolding, no leftover diagnostics, no dead flags.
- Comments state constraints the code can't show — never narration.
- User-facing copy states the thing plainly; no reassurance microcopy.

## Process rules

- Branch from `master`; never commit to it directly.
- `./verify/verify.sh` green before every push. Flaky gate → fix or
  quarantine in the same PR; never route around it.
- After adding/removing/renaming source files, run the stack's
  regeneration step (project gen, lockfile, tidy) and commit the result.
- Commit at boundaries; message says what changed and cites evidence.
- Docs move with behavior — same commit or PR.
- Report outcomes faithfully; failing is failing, with output.
