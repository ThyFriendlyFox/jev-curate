"""TypeSafe Jev client — live API by default when TYPESAFE_API_KEY is set."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any

from typesafe_sdk import Question, TypeSafeClient

from jev_curate.rubric import CurationRubric


class JevClient(ABC):
    @abstractmethod
    def evaluate(
        self,
        state: Any,
        questions: dict[str, Question],
        *,
        model: str,
    ): ...


class LiveJevClient(JevClient):
    """Calls POST /v1/systemone via typesafe-sdk."""

    def __init__(self, api_key: str | None = None, *, timeout: float | None = None) -> None:
        key = api_key or os.environ.get("TYPESAFE_API_KEY")
        if not key:
            raise RuntimeError(
                "TYPESAFE_API_KEY is required for live Jev. "
                "Get a key at https://console.typesafe.ai/settings/keys "
                "or pass --mock only for local tests."
            )
        self._client = TypeSafeClient(api_key=key, timeout=timeout)

    def evaluate(self, state: Any, questions: dict[str, Question], *, model: str):
        return self._client.system_one(state=state, questions=questions, model=model)


def evaluate_rubric(client: JevClient, rubric: CurationRubric, state: Any):
    return client.evaluate(
        state=state,
        questions=rubric.to_jev_questions(),
        model=rubric.model,
    ).answers


BATCH_STATE_KEY = "rows"
BATCH_SEP = "__"


def evaluate_rubric_batch(
    client: JevClient, rubric: CurationRubric, states: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """One Jev call for several rows: every gate is asked once per row key.

    Jev scores each question on its own against the shared state, so each
    question names the one row it judges. Returns answers per row key, by gate name.
    """
    gate_questions = rubric.to_jev_questions()
    questions = {
        f"{key}{BATCH_SEP}{gate}": question.model_copy(
            update={"instructions": f"Judge only the row named {key}. {question.instructions}"}
        )
        for key in states
        for gate, question in gate_questions.items()
    }
    answers = client.evaluate(
        state={BATCH_STATE_KEY: states}, questions=questions, model=rubric.model
    ).answers
    return {
        key: {
            gate: answers[f"{key}{BATCH_SEP}{gate}"]
            for gate in gate_questions
            if f"{key}{BATCH_SEP}{gate}" in answers
        }
        for key in states
    }


def make_client(
    *,
    live: bool,
    gateway: bool = False,
    api_key: str | None = None,
    timeout: float | None = None,
) -> JevClient:
    if not live:
        from jev_curate.mock_client import MockJevClient

        return MockJevClient()
    if gateway:
        from jev_curate.gateway_client import GatewayJevClient

        return GatewayJevClient(api_key=api_key, timeout=timeout)
    return LiveJevClient(api_key=api_key, timeout=timeout)
