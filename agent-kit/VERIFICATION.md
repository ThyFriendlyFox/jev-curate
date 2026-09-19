# VERIFICATION.md — one command answers "is this repo healthy"

`./verify/verify.sh` runs, in order:

1. Lint / format check — `ruff check src tests && ruff format --check src tests`
2. Build — `python -m build --wheel --outdir dist`
3. Tests — `pytest`
4. Repo-specific gates, one script each in `verify/gates/`, each runnable alone:

| Gate | Proves |
|---|---|
| `10_rubric.sh` | `examples/rubric.yaml` parses and `validate-rubric` lists its gates |
| `20_mock_run.sh` | The README quick start works end to end in mock mode: 4 output files, counts add up, every kept row passed, a re-run skips every id, `stats` works |
| `30_live_jev.sh` | `check-jev` makes 1 live call. Skips loudly when `TYPESAFE_API_KEY` is unset |
| `40_agent_kit.sh` | No placeholders remain in the kit; `ROADMAP.md` has a north star and ≥3 ready items |
| `50_docs_cover_options.sh` | Every CLI flag and rubric key has a row in `docs/CONFIGURATION.md` |

`ralph/loop.sh` uses this same command as its exit condition.

## Rules

- CI runs **the same command** as local. No CI-only logic.
- A gate that can't run in some environment **skips loudly**, never
  passes silently.
- New behavior lands with its gate in the same PR whenever feasible.
- A feature's completion promise (ROADMAP.md) should be backed by a gate
  here whenever it can be — evidence that keeps proving itself beats
  evidence produced once.
- Fixing a flaky or broken gate is always in scope, for any task.
