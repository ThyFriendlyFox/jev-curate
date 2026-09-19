# ralph/ — the loop that makes the README true

A Ralph loop feeds one short, fixed prompt to an agent, again and again,
until an objective check passes. The intelligence lives in the repo files,
not in the prompt.

| File | Task |
|---|---|
| `GOAL.md` | What success looks like, one checklist line per README claim, each with its proof |
| `PROMPT.md` | The fixed prompt. Short on purpose. Points at the kit and the goal |
| `loop.sh` | Runs the prompt until `./verify/verify.sh` is green, the agent writes `BLOCKED.md`, or the iteration cap hits |
| `runs/` | Per-run logs. Ignored by git |

## Run it

```sh
pip install -e ".[dev]"
ralph/loop.sh                                   # default: claude -p, 10 iterations
RALPH_MAX_ITERATIONS=3 ralph/loop.sh
RALPH_AGENT_CMD='true' ralph/loop.sh            # dry run: no agent, only the verify check
```

## How it ends

- `verify.sh` green → exit 0. The goal is proven.
- `ralph/BLOCKED.md` exists → exit 2. The agent could not make a line true and said why.
- Cap reached with verify red → exit 1. Read the log.

The weekly cycle in `agent-kit/WEEKLY.md` uses the same loop shape with a
different prompt: ship the top roadmap item instead of the GOAL checklist.
