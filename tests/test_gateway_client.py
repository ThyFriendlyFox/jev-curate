import json
from pathlib import Path
from typing import Any

import httpx2
import pytest
from typesafe_sdk import (
    Choice,
    ChoiceAnswer,
    Noul,
    NoulAnswer,
    Score,
    ScoreAnswer,
    TypeSafeAPIResponseValidationError,
    TypeSafeAuthenticationError,
)

from jev_curate.gateway_client import GATEWAY_URL, GatewayJevClient, gateway_model_id
from jev_curate.pipeline import CurationPipeline, PipelineConfig
from jev_curate.rubric import load_rubric

ROOT = Path(__file__).resolve().parents[1]

QUESTIONS = {
    "valid": Noul(instructions="Coherent text?"),
    "bucket": Choice(instructions="Best category", criteria={"billing": "payments", "tech": None}),
    "quality": Score(instructions="How clear?", criteria=["unclear", "okay", "clear"]),
}

# Shape recorded from a live call to the gateway on 2026-09-19.
GATEWAY_REPLY = {
    "answers": {
        "valid": {"type": "boolean", "probability": 0.96},
        "bucket": {
            "type": "choice",
            "choice": "billing",
            "probabilities": {"billing": 1, "tech": 0},
        },
        "quality": {
            "type": "score",
            "score": 1.99,
            "probabilities": {"0": 0, "1": 0.01, "2": 0.99},
        },
    },
    "usage": {"inputTokens": 376, "outputTokens": 61},
    "warnings": [],
    "providerMetadata": {"typesafe": {"confidence": {"bucket": 1, "quality": 0.99}}},
}


def _client(handler) -> GatewayJevClient:
    return GatewayJevClient(api_key="vck_test", transport=httpx2.MockTransport(handler))


def test_request_uses_the_gateway_protocol():
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json=GATEWAY_REPLY)

    _client(handler).evaluate({"text": "charged twice"}, QUESTIONS, model="jev-latest")

    (request,) = seen
    assert str(request.url) == GATEWAY_URL
    assert request.headers["Authorization"] == "Bearer vck_test"
    assert request.headers["ai-model-id"] == "typesafe-ai/jev"
    assert request.headers["ai-evaluation-model-specification-version"] == "4"
    body = json.loads(request.content)
    assert set(body) == {"state", "questions"}
    assert body["state"] == {"text": "charged twice"}
    assert body["questions"]["valid"] == {"type": "boolean", "instructions": "Coherent text?"}
    assert body["questions"]["bucket"]["criteria"] == {"billing": "payments", "tech": None}
    assert body["questions"]["quality"]["criteria"] == ["unclear", "okay", "clear"]


def test_reply_becomes_native_answers():
    response = _client(lambda request: httpx2.Response(200, json=GATEWAY_REPLY)).evaluate(
        "charged twice", QUESTIONS, model="jev-latest"
    )

    assert response.model == "typesafe-ai/jev"
    assert response.usage.input_tokens == 376
    valid, bucket, quality = (response.answers[k] for k in ("valid", "bucket", "quality"))
    assert isinstance(valid, NoulAnswer) and valid.noul == 0.96
    assert isinstance(bucket, ChoiceAnswer)
    assert (bucket.choice, bucket.confidence) == ("billing", 1.0)
    assert isinstance(quality, ScoreAnswer)
    assert (quality.score, quality.confidence) == (1.99, 0.99)
    assert quality.legend == {0: "unclear", 1: "okay", 2: "clear"}
    assert quality.probabilities == {0: 0.0, 1: 0.01, 2: 0.99}


def test_reply_without_confidence_is_an_error():
    reply = {**GATEWAY_REPLY, "providerMetadata": {}}
    client = _client(lambda request: httpx2.Response(200, json=reply))
    with pytest.raises(TypeSafeAPIResponseValidationError) as exc:
        client.evaluate("charged twice", QUESTIONS, model="jev-latest")
    assert "confidence" in exc.value.field_path


def test_rejected_key_raises_authentication_error():
    reply = {"error": {"message": "Authentication failed.", "type": "authentication_error"}}
    client = _client(lambda request: httpx2.Response(401, json=reply))
    with pytest.raises(TypeSafeAuthenticationError, match="Authentication failed") as exc:
        client.evaluate("charged twice", QUESTIONS, model="jev-latest")
    assert exc.value.endpoint == f"POST {GATEWAY_URL}"


def test_missing_key_fails_plainly(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("AI_GATEWAY_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="AI_GATEWAY_API_KEY"):
        GatewayJevClient()


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        ("jev-latest", "typesafe-ai/jev"),
        ("jev-2", "typesafe-ai/jev-2"),
        ("typesafe-ai/jev", "typesafe-ai/jev"),
    ],
)
def test_gateway_model_id(model: str, expected: str):
    assert gateway_model_id(model) == expected


def _answer_everything(request: httpx2.Request) -> httpx2.Response:
    questions: dict[str, dict[str, Any]] = json.loads(request.content)["questions"]
    answers: dict[str, dict[str, Any]] = {}
    confidence: dict[str, float] = {}
    for name, question in questions.items():
        if question["type"] == "boolean":
            answers[name] = {"type": "boolean", "probability": 0.9}
        else:
            choice = next(iter(question["criteria"]))
            answers[name] = {"type": "choice", "choice": choice, "probabilities": {choice: 0.9}}
            confidence[name] = 0.9
    return httpx2.Response(
        200,
        json={"answers": answers, "providerMetadata": {"typesafe": {"confidence": confidence}}},
    )


def test_pipeline_runs_through_the_gateway_client(tmp_path: Path):
    out = tmp_path / "out"
    stats = CurationPipeline(
        PipelineConfig(
            rubric=load_rubric(ROOT / "examples/rubric.yaml"),
            input_path=ROOT / "examples/corpus.jsonl",
            output_dir=out,
            concurrency=4,
        ),
        client=_client(_answer_everything),
    ).run()

    # Every noul answers yes=0.9, so the max_yes gates reject every row.
    assert (stats.processed, stats.rejected, stats.errors) == (10, 10, 0)
    rejected = [json.loads(line) for line in (out / "rejected.jsonl").read_text().splitlines()]
    assert all("is_ambiguous" in row["_curation"]["failed_gates"] for row in rejected)
    assert len((out / "audit.jsonl").read_text().splitlines()) == 10
