"""Evaluate pass/fail for each gate and overall curation verdict."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from typesafe_sdk import ChoiceAnswer, NoulAnswer, ScoreAnswer

from jev_curate.audit import serialize_answer
from jev_curate.rubric import (
    ChoicePassRule,
    CurationRubric,
    GateSpec,
    NoulPassRule,
    ScorePassRule,
)


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    required: bool
    reason: str
    answer: dict[str, Any]


@dataclass(frozen=True)
class CurationVerdict:
    example_id: str
    kept: bool
    failed_gates: tuple[str, ...]
    gate_results: tuple[GateResult, ...]

    def to_audit_record(self) -> dict[str, Any]:
        return {
            "id": self.example_id,
            "kept": self.kept,
            "failed_gates": list(self.failed_gates),
            "gates": {
                g.name: {
                    "passed": g.passed,
                    "required": g.required,
                    "reason": g.reason,
                    "answer": g.answer,
                }
                for g in self.gate_results
            },
        }


def _default_noul_rule(gate: GateSpec) -> NoulPassRule:
    # "yes means good" gates: default require high yes probability
    lower = gate.name.lower()
    if any(x in lower for x in ("invalid", "ambiguous", "duplicate", "garbled", "bad")):
        return NoulPassRule(max_yes=0.5)
    return NoulPassRule(min_yes=0.5)


def _eval_gate(
    gate: GateSpec,
    answer: NoulAnswer | ChoiceAnswer | ScoreAnswer,
    row: dict[str, Any],
) -> GateResult:
    serialized = serialize_answer(answer)
    rule = gate.pass_rule

    if isinstance(answer, NoulAnswer):
        rule = rule if isinstance(rule, NoulPassRule) else _default_noul_rule(gate)
        passed = rule.check(answer.noul)
        if not passed:
            if rule.min_yes is not None:
                reason = f"yes={answer.noul:.3f} < min_yes={rule.min_yes}"
            else:
                reason = f"yes={answer.noul:.3f} > max_yes={rule.max_yes}"
        else:
            reason = "ok"

    elif isinstance(answer, ChoiceAnswer):
        rule = rule if isinstance(rule, ChoicePassRule) else ChoicePassRule(min_confidence=0.0)
        passed = rule.check(answer.choice, answer.confidence, row)
        reason = "ok" if passed else f"choice={answer.choice!r} confidence={answer.confidence:.3f}"

    elif isinstance(answer, ScoreAnswer):
        rule = rule if isinstance(rule, ScorePassRule) else ScorePassRule()
        passed = rule.check(answer.score, answer.confidence)
        reason = "ok" if passed else f"score={answer.score:.3f} confidence={answer.confidence:.3f}"

    else:
        passed = False
        reason = "unknown answer type"

    return GateResult(
        name=gate.name,
        passed=passed,
        required=gate.required,
        reason=reason,
        answer=serialized,
    )


def evaluate_curation(
    example_id: str,
    rubric: CurationRubric,
    answers: dict[str, NoulAnswer | ChoiceAnswer | ScoreAnswer],
    row: dict[str, Any],
) -> CurationVerdict:
    results: list[GateResult] = []
    failed_required: list[str] = []
    passed_optional = 0
    failed_optional = 0

    gate_by_name = {g.name: g for g in rubric.gates}
    for name, answer in answers.items():
        gate = gate_by_name[name]
        gr = _eval_gate(gate, answer, row)
        results.append(gr)
        if not gr.passed:
            if gr.required:
                failed_required.append(name)
            else:
                failed_optional += 1
        elif not gr.required:
            passed_optional += 1

    if rubric.pass_mode == "all":
        kept = len(failed_required) == 0
    else:
        # any: keep if at least one required gate passed (unusual; for exploratory rubrics)
        required_results = [r for r in results if gate_by_name[r.name].required]
        kept = any(r.passed for r in required_results) if required_results else True

    return CurationVerdict(
        example_id=example_id,
        kept=kept,
        failed_gates=tuple(failed_required),
        gate_results=tuple(results),
    )
