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

## 2026-09-19 — Made a 24.5 s launch video with the /brag skill

I ran the `/brag` skill (latent-spaces/brag) on this repo. It plans a short video and hands a brief to Hyperframes, which renders HTML to MP4. The video opens on row `t006` of `examples/corpus.jsonl`, types the README quick-start command, fills `audit.jsonl` one record per beat, prints the CLI's results table, and ends on the 4 output files. Every figure comes from `jev-curate run --mock` on the example corpus: 10 processed, 3 kept, 7 rejected. The terminal shows the live-mode header the CLI prints; the numbers are the mock's. `npx hyperframes check` passed with 0 errors and 257/257 contrast checks. The output lives in `brag-output/` with the plan, the brief, the composition, the poster, and the share copy. The music bed is not committed; `brag-output/.gitignore` says how to restore it.

Evidence: `brag-output/brag.mp4` (735 frames, 1920x1080, 24.5 s), `brag-output/brag-plan.md`.

## 2026-09-19 — Second brag cut in a different register

The first video was cream paper and a serif. The human asked for a different style and different colors. I made a second cut with the same `/brag` flow in `brag-output-2026-09-19-cinematic/`: deep navy and gold, League Gothic display type, hard cuts on the beat of the vol-1 track at 120 BPM. It opens with 3 slams ("Ten rows." "Three pass." "Seven do not."), stamps row `t006` REJECTED with the audit's 2 real reason strings, runs the command, fills `audit.jsonl` in 2 columns, and lands 3 hero figures (3 kept, 7 rejected, 30.0%). The figures are the same mock run as the first cut. `npx hyperframes check` passed with 0 errors and 141/141 contrast checks after 1 fix: stacked display lines at line-height 0.92 overlapped, so I set it to 1.

Evidence: `brag-output-2026-09-19-cinematic/brag.mp4` (735 frames, 1920x1080, 24.5 s), `brag-output-2026-09-19-cinematic/brag-plan.md`.

## 2026-09-19 — Cinematic cut: music out, drone in

The human liked the cinematic cut but not its music. The `/brag` skill bundles 5 tracks from one upbeat corporate series, and none fits a dark trailer register. I removed the music and generated a bed instead: `composition/scripts/gen_drone.py` writes `assets/drone.wav`, a detuned 55 Hz sub-drone with a slow swell under the run scene and pitch-drop thumps on every cut and slam. The SFX layer is unchanged. The gold light and grid now pulse on the thumps. The bed is generated code, so it is committed; no third-party music remains in that folder.

Evidence: `brag-output-2026-09-19-cinematic/brag.mp4` re-rendered, `npx hyperframes check` green.
