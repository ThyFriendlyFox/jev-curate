# Hyperframes Composition Brief: jev-curate

## Objective
Create a short launch-style brag video for jev-curate.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 24 seconds

## Source Material
- Project root: repo root (`README.md`, `examples/corpus.jsonl`, `examples/rubric.yaml`, `src/jev_curate/cli.py`, `agent-kit/AGENTS.md`)
- Primary files read: README.md, examples/corpus.jsonl, examples/rubric.yaml, cli.py, pipeline.py, gates.py, agent-kit/docs/STYLE.md
- Product name: jev-curate
- Tagline / strongest claim: "Filter with Jev. Train on real outcome labels."
- Key UI or visual moment to recreate: the terminal run (typed quick-start command, CLI header line, Rich results table) and `audit.jsonl` filling line by line
- Copy that must appear verbatim:
  - the t006 row from `examples/corpus.jsonl`
  - `jev-curate run --rubric examples/rubric.yaml --input examples/corpus.jsonl --output .output/run1`
  - `jev-curate rubric='training_example_curation' model=jev-latest mode=live (TypeSafe Jev) concurrency=1`
  - the Curation results table: Processed 10 · Skipped (resume) 0 · Kept → curated.jsonl 3 · Rejected 7 · Errors 0 · Keep rate 30.0%
  - `curated.jsonl`, `rejected.jsonl`, `audit.jsonl`, `errors.jsonl`
  - "Filter with Jev. Train on real outcome labels."

## Creative Direction
- Tone preset: polished
- Creative direction: a terminal that says exactly what it means
- Interpretation: 4 scenes, long holds, `power3.out` / `expo.out` entrances, no overshoot, soft 0.5s crossfades, one coral moment per frame
- Angle: open on the one broken row the example corpus ships with, run the documented command, show the tool's own output rejecting it
- Hook: the t006 row card + "This row is labeled billing."
- Outro / punchline: `$ jev-curate` + "Filter with Jev. Train on real outcome labels."
- Avoid:
  - Generic SaaS language
  - Abstract filler visuals
  - Unrelated visual redesign
  - Any CLI output the CLI does not print

## Visual Identity
- Background: #FAF9F5
- Text: #141413 (ink) on cream; #FAF9F5 on navy
- Accent: #CC785C coral (marks, rules, the "billing" value on navy); #A8542F for coral text on cream
- Code surface: #181715, title bar #252320, hairline rgba(250,249,245,0.14)
- Display font: EB Garamond 400 (renderer-bundled)
- Body font: Inter 400; JetBrains Mono for code and chrome (renderer-bundled)
- Visual references from the project: JSONL rows, the `$` prompt, the Rich box table, the 4-file output table in the README

## Storyboard
Use the storyboard in `brag-output/brag-plan.md` as the creative contract.

Scene summary:
1. The row — 4.5s — t006 card + "This row is labeled billing." + "It is about to be training data."
2. One command — 11.9s — typed command, Enter, header line, 10 audit lines on the beat grid, results table
3. Four files — 4.7s — headline + 4 file cards with real counts
4. Wordmark — 3.4s — `$ jev-curate`, coral rule, tagline, URL

## Audio
- Audio role: warm bed with sparse professional accents
- Audio arc: quiet card → pulse during the run → weighted cards → one bell over the fade
- Music: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`
- Music treatment: data-volume 0.32; automation lane fade-in 0→0.6s, fade-out 22.6→24.0s
- Music cue guidance: `assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json`, 109.96 BPM. Strong-cue locks: 8.74 (first audit line), 13.11 (t009 line; t010 on the next beat 13.64), 19.66 (fourth card). Beat grid: audit lines every beat 8.74→13.64; cards every other beat 16.38→19.66; Enter 8.19; table 14.20; wordmark 20.75; tagline 21.84.
- Audio-reactive treatment: subtle; bass → ✱ mark scale (1.0–1.05), RMS → glow opacity behind content. Data pre-extracted to `assets/audio-data.js` (first 24s, 30 fps, 16 bands).
- Audio-coupled moments:
  - Scene 1 card land — `impact/impactSoft_medium_001.ogg`
  - Scene 1 italic line — `interface/bong_001.ogg`
  - Scene 2 typing — `assets/sfx/typing.wav`, one pre-mixed track built from the bundled `keyboard/keypress-*.wav` set at the exact per-character schedule (`assets/typing-schedule.js`)
  - Scene 2 Enter — `interface/click_003.ogg`
  - Scene 2 audit lines — `interface/click_002.ogg` / `click_005.ogg` alternating, low volume
  - Scene 2 table — `impact/impactSoft_medium_002.ogg`
  - Scene 3 cards — `impactSoft_medium_000/003/004/001` rotating
  - Scene 4 wordmark — `impact/impactBell_heavy_000.ogg`
- SFX selection guidance: low high-frequency-risk files for every repeated moment (per `sfx-analysis.md`); the bell is the only medium-risk sound and it fires once
- SFX analysis guidance: skill `assets/sfx/sfx-analysis.md`
- Exact SFX choice: chosen against the implemented animation, listed above
- Audio files: copied into `brag-output/composition/assets/`

## Hyperframes Instructions
Domain skills loaded: `hyperframes-core`, `hyperframes-animation`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-cli`. /brag is its own workflow; no intent interview.

Requirements:
- Show at least one real UI, copy, or visual element from the source project.
- Keep all text readable in the final render.
- Keep the video within 15-25 seconds.
- Include the planned music/SFX layer.
- Major reveals may move toward nearby strong cues within about 0.15s. Smaller entrances may align to nearby beat points within about 0.10s.
- Use local assets for audio and any required runtime/media dependencies when possible.
- Run `hyperframes check` before render — it is brag's single gate.
