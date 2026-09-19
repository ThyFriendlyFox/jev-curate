from typesafe_sdk import ChoiceAnswer, NoulAnswer, ScoreAnswer

from jev_curate.gates import evaluate_curation
from jev_curate.rubric import (
    ChoicePassRule,
    CurationRubric,
    GateSpec,
    NoulPassRule,
    ScorePassRule,
)


def _rubric() -> CurationRubric:
    return CurationRubric(
        name="t",
        state_field="text",
        gates=(
            GateSpec(
                name="valid",
                kind="noul",
                instructions="valid?",
                pass_rule=NoulPassRule(min_yes=0.8),
            ),
            GateSpec(
                name="ambiguous",
                kind="noul",
                instructions="ambiguous?",
                pass_rule=NoulPassRule(max_yes=0.4),
            ),
        ),
    )


def test_keeps_clean_example():
    row = {"id": "1", "text": "refund please", "label": "billing"}
    answers = {
        "valid": NoulAnswer(noul=0.95),
        "ambiguous": NoulAnswer(noul=0.1),
    }
    v = evaluate_curation("1", _rubric(), answers, row)
    assert v.kept is True
    assert v.failed_gates == ()


def test_rejects_garbled():
    row = {"id": "2", "text": "garbled", "label": "billing"}
    answers = {
        "valid": NoulAnswer(noul=0.2),
        "ambiguous": NoulAnswer(noul=0.1),
    }
    v = evaluate_curation("2", _rubric(), answers, row)
    assert v.kept is False
    assert "valid" in v.failed_gates


def test_choice_match_field():
    rubric = CurationRubric(
        name="t",
        state_field="text",
        gates=(
            GateSpec(
                name="bucket",
                kind="choice",
                instructions="?",
                pass_rule=ChoicePassRule(match_field="label", min_confidence=0.5),
            ),
        ),
    )
    row = {"label": "billing"}
    answers = {
        "bucket": ChoiceAnswer(
            choice="technical",
            confidence=0.9,
            probabilities={"billing": 0.1, "technical": 0.9},
        ),
    }
    v = evaluate_curation("3", rubric, answers, row)
    assert v.kept is False


def test_missing_answer_fails_required_gate():
    row = {"id": "4", "text": "refund please", "label": "billing"}
    answers = {"valid": NoulAnswer(noul=0.95)}  # Jev returned nothing for "ambiguous"
    v = evaluate_curation("4", _rubric(), answers, row)
    assert v.kept is False
    assert v.failed_gates == ("ambiguous",)
    assert v.to_audit_record()["gates"]["ambiguous"]["reason"] == "no answer from Jev"


def test_optional_gate_failure_does_not_reject():
    rubric = CurationRubric(
        name="t",
        state_field="text",
        gates=(
            GateSpec(
                name="valid", kind="noul", instructions="?", pass_rule=NoulPassRule(min_yes=0.8)
            ),
            GateSpec(
                name="dup",
                kind="noul",
                instructions="?",
                pass_rule=NoulPassRule(max_yes=0.3),
                required=False,
            ),
        ),
    )
    answers = {"valid": NoulAnswer(noul=0.9), "dup": NoulAnswer(noul=0.9)}
    v = evaluate_curation("5", rubric, answers, {})
    assert v.kept is True
    assert v.failed_gates == ()
    assert v.to_audit_record()["gates"]["dup"]["passed"] is False


def test_pass_mode_any_keeps_when_one_required_gate_passes():
    rubric = CurationRubric(
        name="t",
        state_field="text",
        pass_mode="any",
        gates=(
            GateSpec(name="a", kind="noul", instructions="?", pass_rule=NoulPassRule(min_yes=0.8)),
            GateSpec(name="b", kind="noul", instructions="?", pass_rule=NoulPassRule(min_yes=0.8)),
        ),
    )
    answers = {"a": NoulAnswer(noul=0.1), "b": NoulAnswer(noul=0.9)}
    assert evaluate_curation("6", rubric, answers, {}).kept is True


def test_score_rule():
    rubric = CurationRubric(
        name="t",
        state_field="text",
        gates=(
            GateSpec(
                name="quality",
                kind="score",
                instructions="?",
                criteria=["poor", "ok", "good"],
                pass_rule=ScorePassRule(min_score=1.5, min_confidence=0.5),
            ),
        ),
    )
    low = ScoreAnswer(
        score=1.0,
        confidence=0.9,
        probabilities={0: 0.05, 1: 0.9, 2: 0.05},
        legend={0: "poor", 1: "ok", 2: "good"},
    )
    high = ScoreAnswer(
        score=1.9,
        confidence=0.9,
        probabilities={0: 0.0, 1: 0.1, 2: 0.9},
        legend={0: "poor", 1: "ok", 2: "good"},
    )
    assert evaluate_curation("7", rubric, {"quality": low}, {}).kept is False
    assert evaluate_curation("8", rubric, {"quality": high}, {}).kept is True
