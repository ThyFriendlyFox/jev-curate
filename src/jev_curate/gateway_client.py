"""Live Jev through Vercel AI Gateway, for accounts that hold a gateway key."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx2
from typesafe_sdk import Question, TypeSafeClient

from jev_curate.client import JevClient

GATEWAY_URL = "https://ai-gateway.vercel.sh/v4/ai/evaluation-model"


def gateway_model_id(model: str) -> str:
    if "/" in model:
        return model
    if model == "jev-latest":
        return "typesafe-ai/jev"
    return f"typesafe-ai/{model}"


def _to_gateway_question(question: dict[str, Any]) -> dict[str, Any]:
    if question["type"] == "noul":
        return {**question, "type": "boolean"}
    return question


def _to_native_answer(
    answer: dict[str, Any], question: dict[str, Any], confidence: float | None
) -> dict[str, Any]:
    if answer["type"] == "boolean":
        return {"type": "noul", "noul": answer["probability"]}
    # confidence stays absent when the gateway omits it; the SDK then rejects the
    # response and the row lands in errors.jsonl instead of passing on a guess.
    native = {**answer} if confidence is None else {**answer, "confidence": confidence}
    native.setdefault("probabilities", {})
    if answer["type"] == "score":
        native["legend"] = {str(i): label for i, label in enumerate(question["criteria"])}
    return native


class GatewayTransport(httpx2.BaseTransport):
    """Rewrites the SDK's POST /v1/systemone into the gateway's evaluation
    protocol and the reply back, so retries, timeouts, and error types stay the SDK's."""

    def __init__(self, inner: httpx2.BaseTransport | None = None) -> None:
        self._inner = inner or httpx2.HTTPTransport()

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        native = json.loads(request.content)
        questions: dict[str, dict[str, Any]] = native["questions"]
        model = gateway_model_id(native["model"])
        outgoing = httpx2.Request(
            "POST",
            GATEWAY_URL,
            headers={
                "Authorization": request.headers["Authorization"],
                "User-Agent": request.headers["User-Agent"],
                "ai-gateway-protocol-version": "0.0.1",
                "ai-gateway-auth-method": "api-key",
                "ai-evaluation-model-specification-version": "4",
                "ai-model-id": model,
            },
            json={
                "state": native["state"],
                "questions": {k: _to_gateway_question(q) for k, q in questions.items()},
            },
            extensions=request.extensions,
        )
        response = self._inner.handle_request(outgoing)
        if response.status_code != 200:
            return response
        response.read()
        body = response.json()
        confidence = body.get("providerMetadata", {}).get("typesafe", {}).get("confidence", {})
        usage = body.get("usage", {})
        return httpx2.Response(
            200,
            request=request,
            json={
                "model": model,
                "usage": {
                    "input_tokens": usage.get("inputTokens"),
                    "output_tokens": usage.get("outputTokens"),
                },
                "answers": {
                    name: _to_native_answer(answer, questions[name], confidence.get(name))
                    for name, answer in body["answers"].items()
                    if name in questions
                },
            },
        )

    def close(self) -> None:
        self._inner.close()


def _name_gateway_endpoint(response: httpx2.Response) -> None:
    # The SDK builds error text from response.request; without this an error
    # line names api.typesafe.ai, a host the call never reached.
    response.request = httpx2.Request("POST", GATEWAY_URL)


class GatewayJevClient(JevClient):
    """Calls Jev as `typesafe-ai/jev` on Vercel AI Gateway."""

    def __init__(
        self, api_key: str | None = None, *, transport: httpx2.BaseTransport | None = None
    ) -> None:
        key = api_key or os.environ.get("AI_GATEWAY_API_KEY")
        if not key:
            raise RuntimeError(
                "AI_GATEWAY_API_KEY is required for --gateway. "
                "Create a key in the Vercel dashboard under AI Gateway."
            )
        self._client = TypeSafeClient(
            api_key=key,
            http_client=httpx2.Client(
                transport=GatewayTransport(transport),
                event_hooks={"response": [_name_gateway_endpoint]},
            ),
        )

    def evaluate(self, state: Any, questions: dict[str, Question], *, model: str):
        return self._client.system_one(state=state, questions=questions, model=model)
