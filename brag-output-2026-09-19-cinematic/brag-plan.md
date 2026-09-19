# Brag Plan: jev-curate (cinematic cut)

Second cut of the jev-curate brag. Same product, same real figures, a different register: dark, big, on the beat.

## What is this app?
jev-curate runs pass/fail gates from a YAML rubric over every training row with TypeSafe Jev, keeps the rows that pass every gate, and writes an audit trail for the rest.

## The angle
Showcase the repository, in the first cut's order and this cut's look. Open on the one broken row the example corpus ships with, run the documented command, let the tool reject the row with its own reason strings, print the CLI's real results table, and end on the rule.

## Hook (first 2-3 seconds)
The t006 record slides in. Condensed display: "THIS ROW IS LABELED BILLING." Then the line the human asked to keep: "It is about to be training data."

## Key moments (the middle)
- The README quick-start command typed fast, Enter, the CLI header line, and `audit.jsonl` filling in two columns, one record every 0.5 s.
- The verdict: row t006 back as a full-width record, a red REJECTED stamp, and the audit's two real reason strings: `transcript_valid: yes=0.043 < min_yes=0.75`, `label_plausible: yes=0.065 < min_yes=0.7`.
- The CLI's own Rich tables (Curation results and Top reject gates) printing line by line, with the four output files and their counts beside them.

## Outro / punchline
"JEV FILTERS." · "IT DOES NOT LABEL." (invariant 2 from agent-kit/AGENTS.md), then `$ jev-curate` and the repo URL.

## User flow worth showing
Row in the corpus → `jev-curate run …` → `audit.jsonl` → the row's verdict → the results table and 4 output files. Scenes 1 to 4.

## Tone
- Preset: cinematic
- Creative direction: a trailer for a filter. Dark room, one gold light, numbers that hit on the kick.
- Interpretation: hard cuts on beats, scale-slam entrances, no crossfades, display type at 300px+, one gold accent per frame plus the red rejection stamp.

## Format: landscape — 1920x1080
## Duration: 35s

## Type floor
No text below 36px, by the human's rule. Where copy did not fit at that size it got its own scene: `audit.jsonl` is 2 scenes of 5 records, the 2 CLI tables are 1 scene each, the 4 files are 1 scene. The video runs 35 s, past the skill's 15-25 s default, on purpose.

## Visual identity (from the project)
No site CSS exists; the terminal is the identity. Palette from the hyperframes-creative Dark / Premium set (row 2).
- Background: #000814
- Panel: #001D3D; hairline rgba(255,195,0,0.16)
- Accent: #FFC300 (gold)
- Text: #E5E5E5; muted #778DA9
- Status: kept #2EC4B6, rejected #FF4D5E
- Display font: League Gothic (bundled, weight 400 only)
- Body font: Inter; code: IBM Plex Mono (both bundled)

## Share copy (draft)
Ten rows in. Three out. jev-curate runs pass/fail gates on every training row with TypeSafe Jev and writes down why the rest were dropped.

## Audio direction
- Role: no music. A generated sub-drone (`composition/scripts/gen_drone.py` → `assets/drone.wav`) with pitch-drop thumps on every cut and slam, a slow swell under the run scene, and silence-shaped SFX on top.
- Music: none. The bundled ende.app tracks were tried (vol-1) and cut at the human's request: the upbeat corporate bed did not fit the register.
- Bed treatment: volume 0.8, fade in 0 to 0.5s, fade out 34.1 to 35s. Thumps at 0.25, 1.15, 2.7, 5.5, 8.0, 10.5, 14.0, 17.5, 17.9, 21.0, 24.5, 27.5, 28.0, 28.5, 29.0, 29.5, 31.5, 31.9, 32.9, 33.5.
- Music cue guidance: none; the cut keeps its own 0.5 s grid (120 BPM feel). Scene cuts on 5.5, 10.5, 14.0, 17.5, 21.0, 24.5, 27.5, 31.5. Audit lines every 0.5 s from 11.0 to 13.0 and 14.5 to 16.5; stamp at 17.9; tables from 21.15 and 24.65; file rows on 28.0 to 29.5; outro lines at 31.9, 32.9, 33.5.
- Audio-reactive treatment: the thumps drive the gold light's intensity, the grid's brightness and the square marks; the drone's RMS drives the vignette. Text scale stays fixed.
- SFX posture: moderate, motion-matched
- Audio-coupled moments: slams (soft impacts), stamp (bell), typing ticks, Enter click, audit-line clicks, figure landings (punch), outro lines (bells)
- Restraint rule: two bells in the outro, nothing else above 0.6

## Storyboard

### Scene 1 — The row — 5.5s (0.0–5.5)
Kicker "■ EXAMPLES/CORPUS.JSONL · LINE 6". The t006 record panel (36px mono) slides up on the right at 0.25. Display headline on the left, word by word from 1.15: "THIS ROW IS LABELED BILLING." with "billing." in gold. At 2.7 the 44px subline: "It is about to be training data."
Sequential/interaction: yes. Audio-coupled idea: soft impacts on the panel and the subline. Transition mood: hard → Scene 2

### Scene 2 — The command — 5.0s (5.5–10.5)
Full-width terminal at 40px. The README command types 5.6 to 7.72, Enter at 8.0, the CLI header prints.
Sequential/interaction: yes, typing and Enter. Audio-coupled idea: keypress ticks, Enter click. Transition mood: hard → Scene 3

### Scene 3 — audit.jsonl, rows 1–5 — 3.5s (10.5–14.0)
Kicker "■ ONE LINE PER EVALUATED ROW". Full-width panel, records t001–t005 at 36px landing every 0.5 s from 11.0; kept teal, rejected red; running tally in the bar.
Sequential/interaction: yes, 5 lines. Audio-coupled idea: click per line. Transition mood: hard → Scene 4

### Scene 4 — audit.jsonl, rows 6–10 — 3.5s (14.0–17.5)
Same panel, records t006–t010 from 14.5; the tally ends at 3 kept · 7 rejected.
Sequential/interaction: yes, 5 lines. Audio-coupled idea: click per line. Transition mood: hard → Scene 5

### Scene 5 — The verdict — 3.5s (17.5–21.0)
Kicker "■ AUDIT.JSONL · T006". The record at 40px. At 17.9 the red REJECTED stamp slams in. At 18.4 and 18.9 the 2 real reason lines print at 40px.
Sequential/interaction: yes. Audio-coupled idea: bell on the stamp, clicks on the lines. Transition mood: hard → Scene 6

### Scene 6 — Curation results — 3.5s (21.0–24.5)
Terminal panel on the left prints the CLI's Curation results table at 36px from 21.15; Keep rate highlights at 22.0. Right: "3 KEPT." (gold) slams at 22.2, "7 REJECTED." snaps in at 22.8.
Sequential/interaction: yes. Audio-coupled idea: punch on the cut, soft impacts on the 2 lines. Transition mood: hard → Scene 7

### Scene 7 — Top reject gates — 3.0s (24.5–27.5)
Terminal panel prints the Top reject gates table from 24.65. Right: "5 GATES." at 25.6, "1 RUBRIC." (gold) at 26.2. Both are true of examples/rubric.yaml.
Sequential/interaction: yes. Audio-coupled idea: punch on the cut, soft impacts. Transition mood: hard → Scene 8

### Scene 8 — Four files — 4.0s (27.5–31.5)
Kicker "■ OUTPUT DIR · .OUTPUT/RUN1". Four full-width rows at 48px mono with 36px descriptions arrive at 28.0, 28.5, 29.0, 29.5: curated.jsonl 3 rows, rejected.jsonl 7 rows, audit.jsonl 10 rows, errors.jsonl 0 rows.
Sequential/interaction: yes. Audio-coupled idea: soft impact per row. Transition mood: hard → Scene 9

### Scene 9 — The rule — 3.5s (31.5–35.0)
"JEV FILTERS." slams at 31.9. "IT DOES NOT LABEL." snaps in gold at 32.9. `$ jev-curate` (72px) and the repo URL (36px) rise at 33.5. The drone fades under the last bell.
Sequential/interaction: yes. Audio-coupled idea: bells at 31.9 and 33.5. Transition mood: hold to end

**Music mood for this video:** none; a dark sub-drone.
**Audio summary:** two thumps under the hook, the drone swells under the run and drops on the verdict, a bell on the stamp, a punch on the results, two bells to close.

## Provenance of figures
Every number and output line comes from `jev-curate run --mock --rubric examples/rubric.yaml --input examples/corpus.jsonl` on the shipped example corpus (the mock is the repo's test fixture). The terminal header is the live-mode string the CLI prints when `TYPESAFE_API_KEY` is set. Reason strings are the audit's `reason` fields, verbatim.
