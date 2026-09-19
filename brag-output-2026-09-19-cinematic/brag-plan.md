# Brag Plan: jev-curate (cinematic cut)

Second cut of the jev-curate brag. Same product, same real figures, a different register: dark, big, on the beat.

## What is this app?
jev-curate runs pass/fail gates from a YAML rubric over every training row with TypeSafe Jev, keeps the rows that pass every gate, and writes an audit trail for the rest.

## The angle
Numbers first. The example run keeps 3 of 10 rows. The video states that in three slams, shows the row that fails hardest with the CLI's own rejection reason, runs the documented command, and lands the totals as hero figures.

## Hook (first 2-3 seconds)
Three condensed lines slam in on the intro: "TEN ROWS." · "THREE PASS." · "SEVEN DO NOT."

## Key moments (the middle)
- Row t006 as a full-width record, then a red REJECTED stamp and the audit's two real reason strings: `transcript_valid: yes=0.043 < min_yes=0.75`, `label_plausible: yes=0.065 < min_yes=0.7`.
- The README quick-start command typed fast, Enter on the beat, the CLI header line.
- `audit.jsonl` filling in two columns, one record every beat at 120 BPM.
- Hero figures: 3 kept, 7 rejected, 30.0% keep rate, then the four output files with their counts.

## Outro / punchline
"JEV FILTERS." · "IT DOES NOT LABEL." (invariant 2 from agent-kit/AGENTS.md), then `$ jev-curate` and the repo URL.

## User flow worth showing
Row in the corpus → `jev-curate run …` → `audit.jsonl` → totals → 4 output files. Scenes 2 to 4.

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
- Role: dense rhythmic bed with big accents
- Music: `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` (most energetic bundled track, 120.19 BPM)
- Music treatment: volume 0.34, fade in 0 to 0.4s, fade out 23.4 to 24.5s
- Music cue guidance: preset `assets/music/cues/happy-beats-business-moves-vol-1-by-ende-dot-app.music-cues.md`. Beat grid starts at 3.02s and runs every 0.5s. Strong-cue locks: 17.02 (figure 1), 18.02 (figure 3), 21.01 (outro line 1), 22.01 (outro line 2), 23.02 (wordmark). Scene cuts on 4.02, 9.02, 16.52, 20.52. Audit lines on every beat 12.02 to 16.52; file rows on 18.52, 19.02, 19.52, 20.02.
- Audio-reactive treatment: expressive on non-text; kick drives the gold light's intensity and the grid's brightness, RMS drives a slow vignette breathe. Text scale stays fixed.
- SFX posture: moderate, motion-matched
- Audio-coupled moments: slams (soft impacts), stamp (bell), typing ticks, Enter click, audit-line clicks, figure landings (punch), outro lines (bells)
- Restraint rule: two bells in the outro, nothing else above 0.6

## Storyboard

### Scene 1 — Three slams — 4.02s (0.00–4.02)
Navy-black ground with a faint gold data grid. "TEN ROWS." slams in at 0.3 (scale + blur). "THREE PASS." snaps in from the left at 1.5, gold. "SEVEN DO NOT." rises with a rotation at 2.6. Hold; gentle breathe.
Sequential/interaction: yes, three phrases with three distinct entrances.
Audio intent: three hits before the beat grid arrives.
Audio-coupled idea: soft impact per slam.
Music: bed, intro
Transition mood: hard → Scene 2

### Scene 2 — The row — 5.0s (4.02–9.02)
Hard cut on the beat. Kicker "■ EXAMPLES/CORPUS.JSONL · T006". A full-width record panel shows the t006 row in large mono, "billing" in gold. At 5.53 a red REJECTED stamp slams in, rotated. At 6.03 and 6.52 the two real reason lines print in red under the record.
Sequential/interaction: yes, stamp then two reason lines.
Audio intent: the stamp is the first big hit.
Audio-coupled idea: bell on the stamp; soft clicks on the reason lines.
Transition mood: hard → Scene 3

### Scene 3 — The run — 7.5s (9.02–16.52)
Hard cut. Terminal panel on top: the README command types 9.10 to 11.22, Enter at 11.52, the CLI header prints. Panel below: `.output/run1/audit.jsonl`, 10 records in two columns landing one per beat 12.02 to 16.52, kept teal, rejected red, running tally in the bar.
Sequential/interaction: yes, typing, Enter, 10 lines.
Audio intent: the pulse.
Audio-coupled idea: keypress ticks, Enter click, click per audit line.
Transition mood: hard → Scene 4

### Scene 4 — The numbers — 4.0s (16.52–20.52)
Hard cut. Three figure lockups: 3 KEPT (gold), 7 REJECTED, 30.0% KEEP RATE, counting up from 17.02, 17.52, 18.02. Below, four mono rows arrive on the beat 18.52 to 20.02: curated.jsonl 3 rows · rejected.jsonl 7 rows · audit.jsonl 10 rows · errors.jsonl 0 rows.
Sequential/interaction: yes, three counters then four rows.
Audio intent: three punches, four ticks.
Audio-coupled idea: punch per figure, soft impact per row.
Transition mood: hard → Scene 5

### Scene 5 — The rule — 3.98s (20.52–24.50)
Hard cut. "JEV FILTERS." slams at 21.01. "IT DOES NOT LABEL." snaps in gold at 22.01. `$ jev-curate` and github.com/ThyFriendlyFox/jev-curate rise at 23.02. Music fades under the last bell.
Sequential/interaction: yes, two lines then the mark.
Audio intent: two bells, then quiet.
Audio-coupled idea: bell at 21.01 and 23.02.
Transition mood: hold to end

**Music mood for this video:** cinematic, driving.
**Audio summary:** three dry hits in the intro, the beat grid takes over for the run, three punches for the figures, two bells to close.

## Provenance of figures
Every number and output line comes from `jev-curate run --mock --rubric examples/rubric.yaml --input examples/corpus.jsonl` on the shipped example corpus (the mock is the repo's test fixture). The terminal header is the live-mode string the CLI prints when `TYPESAFE_API_KEY` is set. Reason strings are the audit's `reason` fields, verbatim.
