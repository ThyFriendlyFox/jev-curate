# Hyperframes Composition Brief: jev-curate (cinematic cut)

## Objective
Create a short cinematic brag video for jev-curate, a second cut in a different visual register from `brag-output/`.

## Output
- Composition directory: `brag-output-2026-09-19-cinematic/composition/`
- Rendered video: `brag-output-2026-09-19-cinematic/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 24.5 seconds

## Source Material
- Project root: repo root
- Primary files read: README.md, examples/corpus.jsonl, examples/rubric.yaml, src/jev_curate/cli.py, agent-kit/AGENTS.md; run output from `jev-curate run --mock` on the example corpus
- Product name: jev-curate
- Tagline / strongest claim: "Jev filters; it does not label." (AGENTS.md invariant 2)
- Key UI or visual moment to recreate: the t006 record with its audit reasons; the terminal run; the results as hero figures
- Copy that must appear verbatim:
  - the t006 row
  - `transcript_valid: yes=0.043 < min_yes=0.75` and `label_plausible: yes=0.065 < min_yes=0.7`
  - `jev-curate run --rubric examples/rubric.yaml --input examples/corpus.jsonl --output .output/run1`
  - `jev-curate rubric='training_example_curation' model=jev-latest mode=live (TypeSafe Jev) concurrency=1`
  - curated.jsonl 3 · rejected.jsonl 7 · audit.jsonl 10 · errors.jsonl 0 · keep rate 30.0%

## Creative Direction
- Tone preset: cinematic
- Creative direction: a trailer for a filter
- Interpretation: hard cuts on beats, scale-slam and side-snap entrances, 300px+ condensed display, gold as the one accent, red only for rejection
- Angle: numbers first, then the row that fails, then the run, then the totals
- Hook: "TEN ROWS." / "THREE PASS." / "SEVEN DO NOT."
- Outro / punchline: "JEV FILTERS." / "IT DOES NOT LABEL."
- Avoid: generic SaaS language, abstract filler, any CLI output the CLI does not print, bouncy eases

## Visual Identity
- Background: #000814; panel #001D3D; hairline rgba(255,195,0,0.16)
- Text: #E5E5E5; muted #778DA9
- Accent: #FFC300; kept #2EC4B6; rejected #FF4D5E
- Display font: League Gothic 400 (bundled)
- Body font: Inter; code: IBM Plex Mono (bundled)

## Storyboard
Use `brag-plan.md` as the creative contract. 1. Three slams 4.02s · 2. The row 5.0s · 3. The run 7.5s · 4. The numbers 4.0s · 5. The rule 3.98s.

## Audio
- Music: none. Bed is a generated sub-drone `assets/drone.wav` (`scripts/gen_drone.py`), data-volume 0.8, lane fade-in 0→0.5, fade-out 23.6→24.5
- Music cue guidance: none; timing grid as listed in the plan
- Audio-reactive: `assets/audio-data.js` extracted from the drone (30 fps); thumps → gold light, grid, square marks; RMS → vignette
- SFX: typing track `assets/sfx/typing.wav` (schedule in `assets/typing-schedule.js`); `interface/click_*` for Enter and audit lines; `impact/impactSoft_medium_*` for slams and rows; `impact/impactPunch_medium_000` for figures; `impact/impactBell_heavy_000/003/004` for the stamp and the outro
- Track allocation: bed 10, SFX 11 and up, no overlapping clips on one index

## Hyperframes Instructions
Domain skills: hyperframes-core, hyperframes-animation, hyperframes-creative, hyperframes-cli. /brag is its own workflow. `npx hyperframes check` is the single gate before render.
