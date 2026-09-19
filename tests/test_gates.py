from typesafe_sdk import ChoiceAnswer, NoulAnswer

from jev_curate.gates import evaluate_curation
from jev_curate.rubric import ChoicePassRule, CurationRubric, GateSpec, NoulPassRule


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
