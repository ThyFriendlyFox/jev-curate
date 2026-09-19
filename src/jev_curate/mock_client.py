"""Mock Jev for unit tests only — production runs should use live Jev."""

from __future__ import annotations

import hashlib
import re
from typing import Any

from typesafe_sdk import (
    Choice,
    ChoiceAnswer,
    Noul,
    NoulAnswer,
    Question,
    Score,
    ScoreAnswer,
    SystemOneResponse,
    Usage,
)

from jev_curate.client import JevClient


class MockJevClient(JevClient):
    _GARBLED = re.compile(r"garbled|hallucin", re.I)
    _AMBIG = re.compile(r"ambiguous|might be| or maybe ", re.I)
    _BILLING = re.compile(r"charge|refund|duplicate|billing", re.I)
    _TECH = re.compile(r"error|500|integration|fail|deploy", re.I)
    _SALES = re.compile(r"pricing|enterprise|seats", re.I)

    def _seed(self, text: str, salt: str) -> float:
        h = hashlib.sha256(f"{salt}:{text}".encode()).hexdigest()
        return int(h[:8], 16) / 0xFFFFFFFF

    def evaluate(self, state: Any, questions: dict[str, Question], *, model: str):
        text = state if isinstance(state, str) else str(state)
        answers: dict = {}
        for name, q in questions.items():
            if isinstance(q, Noul):
                lower = name.lower()
                if "ambiguous" in lower:
                    base = 0.78 if self._AMBIG.search(text) else 0.12
                elif "duplicate" in lower:
                    base = 0.85 if "duplicate" in text.lower() else 0.08
                elif "valid" in lower or "plausible" in lower:
                    base = 0.06 if self._GARBLED.search(text) else 0.96
                    if len(text.strip()) < 12:
                        base = 0.20
                else:
                    base = 0.5
                p = max(0.01, min(0.99, base + (self._seed(text, name) - 0.5) * 0.04))
                answers[name] = NoulAnswer(noul=p)
            elif isinstance(q, Choice):
                scores = {}
                for label in q.criteria:
                    s = 0.05
                    if label == "billing" and self._BILLING.search(text):
                        s += 2.0
                    if label == "technical" and self._TECH.search(text):
                        s += 2.0
                    if label == "sales" and self._SALES.search(text):
                        s += 2.0
                    scores[label] = s + self._seed(text, f"{name}:{label}") * 0.05
                total = sum(scores.values())
                probs = {k: v / total for k, v in scores.items()}
                winner = max(probs, key=probs.get)  # type: ignore[arg-type]
                answers[name] = ChoiceAnswer(
                    choice=winner,
                    confidence=max(probs.values()),
                    probabilities=probs,
                )
            elif isinstance(q, Score):
                answers[name] = ScoreAnswer(
                    score=1.0,
                    confidence=0.9,
                    probabilities={0: 0.05, 1: 0.9, 2: 0.05},
                    legend={0: "a", 1: "b", 2: "c"},
                )
        return SystemOneResponse(
            model=model,
            usage=Usage(input_tokens=len(text.split()), output_tokens=0),
            answers=answers,
        )
