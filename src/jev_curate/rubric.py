"""Load curation rubrics: Jev questions + pass/fail rules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml
from typesafe_sdk import Choice, Noul, Question, Score

PassMode = Literal["all", "any"]


@dataclass(frozen=True)
class NoulPassRule:
    min_yes: float | None = None
    max_yes: float | None = None

    def check(self, probability: float) -> bool:
        if self.min_yes is not None and probability < self.min_yes:
            return False
        if self.max_yes is not None and probability > self.max_yes:
            return False
        return True


@dataclass(frozen=True)
class ChoicePassRule:
    allowed: frozenset[str] | None = None
    min_confidence: float | None = None
    match_field: str | None = None  # row[field] must equal Jev choice

    def check(self, choice: str, confidence: float, row: dict[str, Any]) -> bool:
        if self.min_confidence is not None and confidence < self.min_confidence:
            return False
        if self.allowed is not None and choice not in self.allowed:
            return False
        if self.match_field is not None:
            expected = row.get(self.match_field)
            if expected is not None and str(expected) != choice:
                return False
        return True


@dataclass(frozen=True)
class ScorePassRule:
    min_score: float | None = None
    max_score: float | None = None
    min_confidence: float | None = None

    def check(self, score: float, confidence: float) -> bool:
        if self.min_confidence is not None and confidence < self.min_confidence:
            return False
        if self.min_score is not None and score < self.min_score:
            return False
        if self.max_score is not None and score > self.max_score:
            return False
        return True


@dataclass(frozen=True)
class GateSpec:
    name: str
    kind: str
    instructions: str
    criteria: dict[str, str | None] | list[str] | None = None
    pass_rule: NoulPassRule | ChoicePassRule | ScorePassRule | None = None
    required: bool = True  # if False, failure does not reject (audit only)


@dataclass(frozen=True)
class CurationRubric:
    name: str
    state_field: str
    gates: tuple[GateSpec, ...]
    model: str = "jev-latest"
    pass_mode: PassMode = "all"

    def to_jev_questions(self) -> dict[str, Question]:
        out: dict[str, Question] = {}
        for g in self.gates:
            if g.kind == "noul":
                out[g.name] = Noul(instructions=g.instructions)
            elif g.kind == "choice":
                if not isinstance(g.criteria, dict):
                    raise ValueError(f"Gate {g.name!r} choice requires dict criteria")
                out[g.name] = Choice(instructions=g.instructions, criteria=g.criteria)
            elif g.kind == "score":
                if not isinstance(g.criteria, list):
                    raise ValueError(f"Gate {g.name!r} score requires list criteria")
                out[g.name] = Score(instructions=g.instructions, criteria=g.criteria)
            else:
                raise ValueError(f"Unknown gate kind: {g.kind!r}")
        return out


def _parse_pass_rule(
    kind: str, raw: dict[str, Any] | None
) -> NoulPassRule | ChoicePassRule | ScorePassRule | None:
    if not raw:
        return None
    if kind == "noul":
        return NoulPassRule(
            min_yes=raw.get("min_yes"),
            max_yes=raw.get("max_yes"),
        )
    if kind == "choice":
        allowed = raw.get("allowed")
        return ChoicePassRule(
            allowed=frozenset(allowed) if allowed else None,
            min_confidence=raw.get("min_confidence"),
            match_field=raw.get("match_field"),
        )
    if kind == "score":
        return ScorePassRule(
            min_score=raw.get("min_score"),
            max_score=raw.get("max_score"),
            min_confidence=raw.get("min_confidence"),
        )
    raise ValueError(f"Unknown kind for pass rule: {kind!r}")


def load_rubric(path: str | Path) -> CurationRubric:
    data = yaml.safe_load(Path(path).read_text())
    if not isinstance(data, dict):
        raise ValueError("Rubric YAML must be a mapping")

    gates_raw = data.get("gates") or data.get("questions") or []
    gates: list[GateSpec] = []
    for g in gates_raw:
        kind = g["type"]
        gates.append(
            GateSpec(
                name=g["name"],
                kind=kind,
                instructions=g["instructions"],
                criteria=g.get("criteria"),
                pass_rule=_parse_pass_rule(kind, g.get("pass")),
                required=bool(g.get("required", True)),
            )
        )
    if not gates:
        raise ValueError("Rubric must define at least one gate")

    return CurationRubric(
        name=data.get("name", Path(path).stem),
        state_field=data.get("state_field", "text"),
        gates=tuple(gates),
        model=data.get("model", "jev-latest"),
        pass_mode=data.get("pass_mode", "all"),
    )
