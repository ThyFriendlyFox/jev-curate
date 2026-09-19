"""Serialize Jev answers for audit trails."""

from __future__ import annotations

from typing import Any

from typesafe_sdk import ChoiceAnswer, NoulAnswer, ScoreAnswer


def serialize_answer(answer: NoulAnswer | ChoiceAnswer | ScoreAnswer) -> dict[str, Any]:
    if isinstance(answer, NoulAnswer):
        return {"type": "noul", "yes": answer.noul, "no": 1.0 - answer.noul}
    if isinstance(answer, ChoiceAnswer):
        return {
            "type": "choice",
            "choice": answer.choice,
            "confidence": answer.confidence,
            "probabilities": dict(answer.probabilities),
        }
    return {
        "type": "score",
        "score": answer.score,
        "confidence": answer.confidence,
        "probabilities": {str(k): v for k, v in answer.probabilities.items()},
    }
