"""Resumable JSONL curation pipeline."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from typesafe_sdk import TypeSafeAuthenticationError

from jev_curate.client import JevClient, evaluate_rubric
from jev_curate.gates import CurationVerdict, evaluate_curation
from jev_curate.rubric import CurationRubric


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open() as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON") from exc


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_done_ids(*paths: Path) -> set[str]:
    done: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        for row in read_jsonl(path):
            rid = row.get("id") or row.get("record", {}).get("id")
            if rid is not None:
                done.add(str(rid))
    return done


@dataclass
class PipelineStats:
    processed: int = 0
    skipped: int = 0
    kept: int = 0
    rejected: int = 0
    errors: int = 0
    reject_reasons: Counter = field(default_factory=Counter)


@dataclass
class PipelineConfig:
    rubric: CurationRubric
    input_path: Path
    output_dir: Path
    limit: int | None = None  # max rows evaluated this run (skipped rows do not count)
    concurrency: int = 1  # parallel Jev calls; writes stay on the calling thread
    retry_errors: bool = False  # re-evaluate ids present only in errors.jsonl


@dataclass(frozen=True)
class _Outcome:
    ex_id: str
    row: dict[str, Any]
    state: Any = None
    verdict: CurationVerdict | None = None
    error: Exception | None = None


def _example_id(row: dict[str, Any], index: int) -> str:
    return str(row.get("id", index))


def _extract_state(row: dict[str, Any], rubric: CurationRubric) -> Any:
    if "state" in row:
        return row["state"]
    if rubric.state_field in row:
        primary = row[rubric.state_field]
        # Include common metadata so gates can judge label plausibility, etc.
        extra = {k: v for k, v in row.items() if k not in ("id", "meta", rubric.state_field)}
        if extra and isinstance(primary, str):
            return {rubric.state_field: primary, **extra}
        return primary
    return {k: v for k, v in row.items() if k not in ("id", "meta")}


class CurationPipeline:
    def __init__(self, config: PipelineConfig, client: JevClient) -> None:
        self.config = config
        self.client = client
        self.output_dir = config.output_dir
        self.curated_path = self.output_dir / "curated.jsonl"
        self.rejected_path = self.output_dir / "rejected.jsonl"
        self.audit_path = self.output_dir / "audit.jsonl"
        self.errors_path = self.output_dir / "errors.jsonl"

    def run(self) -> PipelineStats:
        stats = PipelineStats()
        done_paths = [self.curated_path, self.rejected_path]
        if not self.config.retry_errors:
            done_paths.append(self.errors_path)
        done = load_done_ids(*done_paths)
        pending = self._pending(done, stats)

        workers = max(1, self.config.concurrency)
        if workers == 1:
            for ex_id, row in pending:
                self._record(self._evaluate(ex_id, row), stats)
            return stats

        # Only the calling thread appends to the output files, so records never interleave.
        with ThreadPoolExecutor(max_workers=workers) as pool:
            in_flight: set[Future[_Outcome]] = set()
            try:
                for ex_id, row in pending:
                    in_flight.add(pool.submit(self._evaluate, ex_id, row))
                    if len(in_flight) >= workers * 2:
                        in_flight = self._drain(in_flight, stats)
                while in_flight:
                    in_flight = self._drain(in_flight, stats)
            except BaseException:
                pool.shutdown(wait=False, cancel_futures=True)
                raise
        return stats

    def _pending(self, done: set[str], stats: PipelineStats) -> Iterator[tuple[str, dict]]:
        submitted = 0
        for index, row in enumerate(read_jsonl(self.config.input_path)):
            if self.config.limit is not None and submitted >= self.config.limit:
                break
            ex_id = _example_id(row, index)
            if ex_id in done:
                stats.skipped += 1
                continue
            submitted += 1
            yield ex_id, row

    def _drain(self, in_flight: set[Future[_Outcome]], stats: PipelineStats) -> set:
        finished, remaining = wait(in_flight, return_when=FIRST_COMPLETED)
        for fut in finished:
            self._record(fut.result(), stats)
        return remaining

    def _evaluate(self, ex_id: str, row: dict[str, Any]) -> _Outcome:
        try:
            state = _extract_state(row, self.config.rubric)
            answers = evaluate_rubric(self.client, self.config.rubric, state)
            verdict = evaluate_curation(ex_id, self.config.rubric, answers, row)
            return _Outcome(ex_id, row, state=state, verdict=verdict)
        except TypeSafeAuthenticationError:
            # A bad key fails every row; stop the run instead of writing N error records.
            raise
        except Exception as exc:  # noqa: BLE001
            return _Outcome(ex_id, row, error=exc)

    def _record(self, outcome: _Outcome, stats: PipelineStats) -> None:
        if outcome.error is not None:
            append_jsonl(
                self.errors_path,
                {"id": outcome.ex_id, "error": str(outcome.error), "row": outcome.row},
            )
            stats.errors += 1
            return
        assert outcome.verdict is not None
        self._write(outcome.ex_id, outcome.row, outcome.state, outcome.verdict, stats)
        stats.processed += 1

    def _write(
        self,
        ex_id: str,
        row: dict[str, Any],
        state: Any,
        verdict: CurationVerdict,
        stats: PipelineStats,
    ) -> None:
        audit = verdict.to_audit_record()
        audit["state"] = state
        append_jsonl(self.audit_path, audit)

        payload = {**row, "_curation": audit}
        if verdict.kept:
            append_jsonl(self.curated_path, payload)
            stats.kept += 1
        else:
            append_jsonl(self.rejected_path, payload)
            stats.rejected += 1
            for gate in verdict.failed_gates:
                stats.reject_reasons[gate] += 1


def summarize(output_dir: Path) -> dict[str, Any]:
    counts = {}
    for name in ("curated", "rejected", "audit", "errors"):
        p = output_dir / f"{name}.jsonl"
        counts[name] = sum(1 for _ in read_jsonl(p)) if p.exists() else 0
    total = counts["curated"] + counts["rejected"]
    return {
        **counts,
        "keep_rate": counts["curated"] / total if total else 0.0,
    }
