# Brag Plan: jev-curate

## What is this app?
jev-curate is a Python CLI that runs pass/fail gates from a YAML rubric over every row of a training corpus with TypeSafe Jev, keeps the rows that pass every gate, and writes an audit trail for the rest. The pitch is discipline: Jev filters, it does not label.

## The angle
The repo ships a 10-row example corpus with one deliberately broken row: `t006`, a garbled transcript labeled `billing`. The video opens on that row, exactly as it sits in `examples/corpus.jsonl`, then runs the documented quick-start command and lets the tool's own output do the talking. No claims the CLI does not print.

## Hook (first 2-3 seconds)
A navy code card slides up with the real row: `{"id": "t006", "text": "[garbled hallucinated transcript] the the the subscription music playing silence", "label": "billing"}`. Serif headline: "This row is labeled billing." Beat. Italic: "It is about to be training data."

## Key moments (the middle)
- The quick-start command from the README typed live, 4 lines with `\` continuations, then Enter.
- `audit.jsonl` filling one line per beat, 10 real audit records from a run on the example corpus, `"kept": true` in green, `"kept": false` in red.
- The CLI's own Rich table printing: Processed 10, Kept 3, Rejected 7, Keep rate 30.0%.
- Four output-file cards arriving one by one with the real row counts: curated 3, rejected 7, audit 10, errors 0.

## Outro / punchline
`$ jev-curate` wordmark, then the README's own line verbatim: "Filter with Jev. Train on real outcome labels." Repo URL underneath.

## User flow worth showing
Entry: the row in the corpus → key action: `jev-curate run --rubric … --input … --output …` → result: `audit.jsonl` streaming, the results table, the 4 output files. This is the centerpiece (scene 2 and 3).

## Tone
- Preset: polished
- Creative direction: a terminal that says exactly what it means. Simplified Technical English on cream paper.
- Interpretation: few scenes, long holds, no overshoot eases, one accent per frame. Motion is fast-in then hold. The copy is the repo's copy.

## Format: landscape — 1920x1080
## Duration: 24s

## Visual identity (from the project)
The project is a CLI with no site CSS. Its identity is the README and the terminal. Palette and type are adopted from the HyperFrames `code-editorial` frame preset because it is built for exactly this material (a warm-navy code surface on cream paper).
- Background: #FAF9F5 (cream)
- Accent: #CC785C (coral) for marks and rules; #A8542F for coral text on cream (WCAG AA)
- Text: #141413 (ink); #FAF9F5 on the navy code surface
- Code surface: #181715 (navy), #252320 title bar; syntax teal #5DB8A6, amber #E8A55A, success #5DB872, fail #E06666
- Display font: EB Garamond 400 (bundled by the renderer)
- Body font: Inter 400; code and chrome: JetBrains Mono (both bundled)
- Strongest visual element: the JSONL row and the terminal output

## Share copy (draft)
jev-curate: pass/fail gates on every training row with TypeSafe Jev. Keep what passes, audit the rest. Jev filters. It does not label.

## Audio direction
- Role: warm bed with sparse professional accents
- Music: `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` (steady, clean; the polished pick)
- Music treatment: start at 0, volume 0.32, fade in 0 to 0.6s, fade out 22.6 to 24.0s. The final bell rings over the fade.
- Music cue guidance: preset `assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.md`, 109.96 BPM. Strong cues to lock: 8.74s (first audit line), 13.11s (last audit line), 19.66s (fourth file card). Beat-grid windows: audit lines on every beat 8.74 to 13.64; file cards on every other beat 16.38, 17.47, 18.56, 19.66; Enter at 8.19; table at 14.20; wordmark at 20.75.
- Audio-reactive treatment: subtle. Bass drives the coral ✱ mark scale (±5%) and a warm glow opacity behind the content. No waveforms, no bars.
- SFX posture: sparse, motion-matched, low high-frequency risk.
- Audio-coupled moments: typed command with keypress ticks; audit lines with soft clicks on the beat grid; table print with a soft impact; cards with soft impacts; wordmark with one bell.
- Restraint rule: nothing above 0.6 volume except the final bell. No sound on text fades.

## Storyboard

### Scene 1 — The row — 4.5s (0.0–4.5)
Cream ground, mono kicker top-left "✱ EXAMPLES/CORPUS.JSONL · LINE 6". A navy code card (right half) slides up with the real t006 row, JSON syntax colored, "billing" in coral. Headline left (EB Garamond): "This row is labeled billing." Italic second line: "It is about to be training data."
Sequential/interaction: none. Card lands, then two lines.
Audio intent: quiet arrival, a dry accent on the second line.
Audio-coupled idea: card land impact at 0.25s; soft bong on the italic line.
Music: bed at 0.32
Transition mood: soft → Scene 2

### Scene 2 — One command — 11.9s (4.5–16.4)
Split frame. Left: a terminal window (title "bash — jev-curate"). The README quick-start command types character by character from 4.9s to 7.9s, 4 lines with `\` continuations. Enter at 8.19s. The CLI header line prints: `jev-curate rubric='training_example_curation' model=jev-latest mode=live (TypeSafe Jev) concurrency=1`. Right: a panel titled `.output/run1/audit.jsonl`. From 8.74s one audit line lands per beat, 10 lines, `"kept": true` green, `"kept": false` red, ending on the 13.11s strong cue with t010 at 13.64. At 14.20 the terminal prints the CLI's Rich table with the real figures. Hold to 16.4.
Sequential/interaction: yes. Typed command, Enter, 10 audit lines one by one, table printed line by line.
Audio intent: the run has a pulse. Ticks on the grid.
Audio-coupled idea: keypress ticks per character; click on Enter; soft click per audit line; soft impact on the table.
Music: bed
Transition mood: soft → Scene 3

### Scene 3 — Four files — 4.7s (16.4–21.1, crossfade 20.6–21.1)
Kicker "✱ OUTPUT DIR · .OUTPUT/RUN1". Headline: "Four files. Every row lands in one." Four hairline cards arrive one by one: curated.jsonl (3 rows, "Passed every required gate. Train on this."), rejected.jsonl (7 rows, "Failed rows with a _curation record: which gate, Jev probabilities."), audit.jsonl (10 rows, "One line per evaluated row, kept or not."), errors.jsonl (0 rows, "API and parse failures. A re-run skips them unless --retry-errors."). Each card holds ≥1s before the next.
Sequential/interaction: yes, 4 cards at 16.38, 17.47, 18.56, 19.66.
Audio intent: each card has weight.
Audio-coupled idea: soft impact per card on the beat.
Music: bed
Transition mood: soft → Scene 4

### Scene 4 — Wordmark — 3.4s (20.6–24.0)
`$ jev-curate` in mono, large, lands at 20.75. Coral rule draws on. Italic tagline at 21.84: "Filter with Jev. Train on real outcome labels." Mono URL: github.com/ThyFriendlyFox/jev-curate. Hold. Music fades out under the bell.
Sequential/interaction: none
Audio intent: one clean landing.
Audio-coupled idea: bell at 20.75, music fade from 22.6.
Music: bed fading to 0 at 24.0
Transition mood: hold to end

**Music mood for this video:** polished, steady.
**Audio summary:** a warm bed enters under a quiet card, gains a pulse while the run streams on the beat grid, and resolves with one bell over the fade.

## Provenance of figures
Every number and every line of output shown comes from `jev-curate run --mock --rubric examples/rubric.yaml --input examples/corpus.jsonl` on the repo's shipped example corpus (the mock is the repo's test fixture tuned to that corpus). The terminal header shows the live-mode string the CLI prints when `TYPESAFE_API_KEY` is set. No figure is invented.
