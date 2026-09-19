# Changelog

All notable changes to jev-curate are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/).

## [Unreleased]
### Added
- `run --concurrency N` runs N parallel Jev calls. Output files are written by one thread.
- `run --retry-errors` re-evaluates ids that are only in `errors.jsonl`.
- `./verify/verify.sh`: one command for lint, build, tests, and 5 repo gates. CI runs the same script.
- `agent-kit/`: the operating manual for agents and humans working on this repo.
- `ralph/`: a Ralph loop with the README as its goal.
- Tests for missing answers, optional gates, `pass_mode: any`, score rules, resume, limit, concurrency, retry, auth failure, and the CLI.
### Changed
- A gate that Jev did not answer now fails closed. Before, it was silently absent from the verdict.
- `--limit N` counts rows evaluated this run. Skipped rows do not count.
- `check-jev` and `run` report a missing or rejected API key as one line, not a traceback.
### Deprecated
### Removed
### Fixed
- A bad API key stops the run at once instead of writing one error row per input row.
### Security
