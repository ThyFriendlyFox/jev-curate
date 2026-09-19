# DEVLOG.md — the live devlog

The plain history of this project. A person who knows nothing about the
code reads this file and knows what happened, in order, with no jargon.
Append only. Never rewrite an old entry — a wrong entry gets a
correction entry, not an edit.

Write every entry in the voice of `TONE.md`.

## Entry shape

Every entry has the same shape:

```
## YYYY-MM-DD — <one line: what happened>

<What we did. What worked. What broke. What we learned.
3–10 short sentences. Plain words. Past tense for what happened,
present tense for how things now stand.>

Evidence: <commit / tag / gate run / screenshot>
```

## When to write

- Every WEEKLY.md cycle writes one entry at step 5 (before merge).
- A failed or abandoned attempt gets an entry too. The devlog records
  what happened, not what succeeded. A week with no shipped feature
  still gets its entry.
- Out-of-band work (security patch, gate repair, big triage) gets one.
- SETUP.md writes the first entry: "Installed the agent kit."

## What does not go here

- Code detail that belongs in commit messages.
- Promises about the future — that is ROADMAP.md.
- State claims — that is STATUS.md. The devlog is the story; STATUS is
  the snapshot.

---

## 2026-09-19 — Reached live Jev through Vercel AI Gateway

The human holds a Vercel AI Gateway key, not a TypeSafe key. The gateway
serves Jev as `typesafe-ai/jev`, but it does not speak `/v1/systemone`. Vercel
documents the TypeScript AI SDK only, so I read the wire format from the
`@ai-sdk/gateway` 4.0.87 source and confirmed it with 1 live request. I wrote
`GatewayJevClient`: a transport that rewrites each `typesafe-sdk` request and
reply, so retries and error types stay the SDK's. The first live call in this
repo's history worked: `check-jev --gateway` returned `ok.noul=0.990`. A bad
key stopped the run with 1 line. The first version named `api.typesafe.ai` in
gateway errors; I fixed that with a response hook. The free tier broke the
full run: 4 of 10 rows evaluated, then 429 for every call. My own probing
used part of that quota. Gate 30 now skips loudly on a gateway 429.

Evidence: `tests/test_gateway_client.py` (9 tests); `./verify/verify.sh` green with 30 tests; `.output/gateway1` holds the 4 live rows.

<!-- Entries below, newest first. -->

## 2026-09-19 — Ran the Ralph loop until the README was true

The README described a tool; the code was close but had no proof. I wrote
`ralph/GOAL.md` with 16 lines, one per README claim, each naming its proof.
I wrote `verify/verify.sh` and 5 gates so the loop has an objective exit.
The first verify run was red on 2 gates: the kit still had placeholders and
no option was documented. Gate 40 also passed with placeholders present
because `pipefail` hid a grep match; I fixed the gate before trusting it.
Code changed in 4 places. An unanswered gate now fails closed. `--concurrency`
is real, with one writer thread. `--retry-errors` re-runs errored ids. A bad
key stops the run at once. Tests went from 4 to 18. I did not exercise live
Jev: this environment has no `TYPESAFE_API_KEY`, so gate 30 skipped loudly.
I ran the loop's iterations by hand in this session; `ralph/loop.sh` drives
`claude -p` for the next person.

Evidence: `./verify/verify.sh` green (lint, build, 18 tests, 5 gates, 1 skip); `ralph/GOAL.md`.

## 2026-09-19 — Installed the agent kit

jev-curate is a CLI that filters a JSONL training corpus with TypeSafe Jev
pass/fail gates and writes curated, rejected, audit, and error files. I
unpacked the kit into `agent-kit/`, filled every placeholder, and wrote the
contract, docs, CI workflows, and a seeded roadmap. The queue holds 4
provisional items: `merge`, a token and cost report, retry policy flags,
and a review sample. The blog-post skill is at `.claude/skills/blog-post/`.
The kit's `ADAPTERS.md` is now `CLIENTS.md`, because the seam here is the
Jev client (live or mock).

Evidence: gate `40_agent_kit` green; `agent-kit/ROADMAP.md` Feature Queue.
