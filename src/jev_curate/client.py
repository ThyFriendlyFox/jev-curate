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
    ):
        ...


class LiveJevClient(JevClient):
    """Calls POST /v1/systemone via typesafe-sdk."""

    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.environ.get("TYPESAFE_API_KEY")
        if not key:
            raise RuntimeError(
                "TYPESAFE_API_KEY is required for live Jev. "
                "Get a key at https://console.typesafe.ai/settings/keys "
                "or pass --mock only for local tests."
            )
        self._client = TypeSafeClient(api_key=key)

    def evaluate(self, state: Any, questions: dict[str, Question], *, model: str):
        return self._client.system_one(state=state, questions=questions, model=model)


def evaluate_rubric(client: JevClient, rubric: CurationRubric, state: Any):
    return client.evaluate(
        state=state,
        questions=rubric.to_jev_questions(),
        model=rubric.model,
    ).answers


def make_client(*, live: bool, api_key: str | None = None) -> JevClient:
    if not live:
        from jev_curate.mock_client import MockJevClient

        return MockJevClient()
    return LiveJevClient(api_key=api_key)
