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
## Duration: 24.5s

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
- Bed treatment: volume 0.8, fade in 0 to 0.5s, fade out 23.6 to 24.5s. Thumps at 0.25, 1.15, 2.7, 5.0, 7.5, 13.5, 13.9, 17.0, 18.5, 19.0, 19.5, 20.0, 21.5, 21.9, 22.9, 23.5.
- Music cue guidance: none; the cut keeps its own 0.5 s grid (120 BPM feel). Scene cuts on 5.0, 13.5, 17.0, 21.5. Audit lines every 0.5 s from 8.0 to 12.5; stamp at 13.9; table from 17.15; file rows on 18.5, 19.0, 19.5, 20.0; outro lines at 21.9, 22.9, 23.5.
- Audio-reactive treatment: the thumps drive the gold light's intensity, the grid's brightness and the square marks; the drone's RMS drives the vignette. Text scale stays fixed.
- SFX posture: moderate, motion-matched
- Audio-coupled moments: slams (soft impacts), stamp (bell), typing ticks, Enter click, audit-line clicks, figure landings (punch), outro lines (bells)
- Restraint rule: two bells in the outro, nothing else above 0.6

## Storyboard

### Scene 1 — The row — 5.0s (0.00–5.00)
Kicker "■ EXAMPLES/CORPUS.JSONL · LINE 6". The t006 record panel slides up on the right at 0.25. Display headline on the left, word by word from 1.15: "THIS ROW IS LABELED BILLING." with "billing." in gold. At 2.7 the mono subline: "It is about to be training data."
Sequential/interaction: yes, panel, then five words, then the subline.
Audio intent: a thump on the panel, a thump on the subline.
Audio-coupled idea: soft impacts on both.
Transition mood: hard → Scene 2

### Scene 2 — The run — 8.5s (5.00–13.50)
Hard cut. Terminal panel on top: the README command types 5.10 to 7.22, Enter at 7.5, the CLI header prints. Panel below: `.output/run1/audit.jsonl`, 10 records in two columns landing every 0.5 s from 8.0 to 12.5, kept teal, rejected red, running tally in the bar.
Sequential/interaction: yes, typing, Enter, 10 lines.
Audio intent: the drone swells under the run.
Audio-coupled idea: keypress ticks, Enter click, click per audit line.
Transition mood: hard → Scene 3

### Scene 3 — The verdict — 3.5s (13.50–17.00)
Hard cut, the swell drops. Kicker "■ AUDIT.JSONL · T006". The t006 record full width. At 13.9 the red REJECTED stamp slams in, rotated. At 14.4 and 14.9 the two real reason lines print in red.
Sequential/interaction: yes, stamp then two lines.
Audio intent: the big hit.
Audio-coupled idea: bell on the stamp, clicks on the lines.
Transition mood: hard → Scene 4

### Scene 4 — The results — 4.5s (17.00–21.50)
Hard cut. Kicker "■ CURATION RESULTS · .OUTPUT/RUN1". Terminal panel on the left prints the CLI's two Rich tables line by line from 17.15; the Keep rate row highlights at 18.4. Right column: four file rows arrive at 18.5, 19.0, 19.5, 20.0: curated.jsonl 3 rows, rejected.jsonl 7 rows, audit.jsonl 10 rows, errors.jsonl 0 rows, each with its README description.
Sequential/interaction: yes, table print then four rows.
Audio intent: a punch on the cut, soft impacts on the rows.
Transition mood: hard → Scene 5

### Scene 5 — The rule — 3.0s (21.50–24.50)
Hard cut. "JEV FILTERS." slams at 21.9. "IT DOES NOT LABEL." snaps in gold at 22.9. `$ jev-curate` and the repo URL rise at 23.5. The drone fades under the last bell.
Sequential/interaction: yes, two lines then the mark.
Audio intent: two bells, then quiet.
Transition mood: hold to end

**Music mood for this video:** none; a dark sub-drone.
**Audio summary:** two thumps under the hook, the drone swells under the run and drops on the verdict, a bell on the stamp, a punch on the results, two bells to close.

## Provenance of figures
Every number and output line comes from `jev-curate run --mock --rubric examples/rubric.yaml --input examples/corpus.jsonl` on the shipped example corpus (the mock is the repo's test fixture). The terminal header is the live-mode string the CLI prints when `TYPESAFE_API_KEY` is set. Reason strings are the audit's `reason` fields, verbatim.
