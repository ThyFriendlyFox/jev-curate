"""Resumable JSONL curation pipeline."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

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
    limit: int | None = None
    concurrency: int = 1  # reserved for future async batching


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
        done = load_done_ids(self.curated_path, self.rejected_path, self.errors_path)

        for index, row in enumerate(read_jsonl(self.config.input_path)):
            if self.config.limit is not None and stats.processed >= self.config.limit:
                break

            ex_id = _example_id(row, index)
            if ex_id in done:
                stats.skipped += 1
                continue

            try:
                state = _extract_state(row, self.config.rubric)
                answers = evaluate_rubric(self.client, self.config.rubric, state)
                verdict = evaluate_curation(ex_id, self.config.rubric, answers, row)
                self._write(ex_id, row, state, verdict, stats)
                stats.processed += 1
            except Exception as exc:  # noqa: BLE001
                append_jsonl(
                    self.errors_path,
                    {"id": ex_id, "error": str(exc), "row": row},
                )
                stats.errors += 1

        return stats

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
