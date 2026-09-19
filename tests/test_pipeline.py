import json
from pathlib import Path
from typing import Any

import httpx2
import pytest
from typesafe_sdk import Question, TypeSafeAuthenticationError

from jev_curate.client import JevClient, make_client
from jev_curate.pipeline import CurationPipeline, PipelineConfig, summarize
from jev_curate.rubric import load_rubric

ROOT = Path(__file__).resolve().parents[1]
RUBRIC = ROOT / "examples" / "rubric.yaml"
CORPUS = ROOT / "examples" / "corpus.jsonl"


def _ids(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [json.loads(line)["id"] for line in path.read_text().splitlines() if line.strip()]


def _run(out: Path, client: JevClient | None = None, **cfg: Any):
    pipeline = CurationPipeline(
        PipelineConfig(rubric=load_rubric(RUBRIC), input_path=CORPUS, output_dir=out, **cfg),
        client=client or make_client(live=False),
    )
    return pipeline.run()


class _FlakyOnce(JevClient):
    """Fails the first call for one id, then behaves like the mock."""

    def __init__(self, fail_text: str) -> None:
        self._inner = make_client(live=False)
        self._fail_text = fail_text
        self.failed = False

    def evaluate(self, state: Any, questions: dict[str, Question], *, model: str):
        if not self.failed and self._fail_text in str(state):
            self.failed = True
            raise RuntimeError("simulated transient API failure")
        return self._inner.evaluate(state, questions, model=model)


class _BadKey(JevClient):
    def __init__(self) -> None:
        self.calls = 0

    def evaluate(self, state: Any, questions: dict[str, Question], *, model: str):
        self.calls += 1
        raise TypeSafeAuthenticationError(
            401, {"error": "invalid key"}, httpx2.Headers(), "invalid key"
        )


def test_pipeline_mock(tmp_path: Path):
    out = tmp_path / "out"
    stats = _run(out)
    assert stats.processed == 10
    s = summarize(out)
    assert s["curated"] + s["rejected"] == 10
    assert (out / "audit.jsonl").exists()


def test_pipeline_resume_skips_done_ids(tmp_path: Path):
    out = tmp_path / "out"
    _run(out)
    stats = _run(out)
    assert stats.skipped == 10
    assert stats.processed == 0
    assert summarize(out)["audit"] == 10


def test_pipeline_limit_counts_evaluated_rows(tmp_path: Path):
    out = tmp_path / "out"
    assert _run(out, limit=3).processed == 3
    second = _run(out, limit=3)
    assert second.skipped == 3
    assert second.processed == 3


def test_pipeline_concurrency_matches_sequential(tmp_path: Path):
    seq = tmp_path / "seq"
    par = tmp_path / "par"
    _run(seq)
    stats = _run(par, concurrency=4)
    assert stats.processed == 10
    assert stats.errors == 0
    assert sorted(_ids(par / "curated.jsonl")) == sorted(_ids(seq / "curated.jsonl"))
    assert sorted(_ids(par / "rejected.jsonl")) == sorted(_ids(seq / "rejected.jsonl"))
    assert len(_ids(par / "audit.jsonl")) == 10


def test_retry_errors(tmp_path: Path):
    out = tmp_path / "out"
    stats = _run(out, client=_FlakyOnce("enterprise plan"))
    assert stats.errors == 1
    assert stats.processed == 9
    assert _ids(out / "errors.jsonl") == ["t003"]

    # Default: an errored id counts as done and is skipped.
    assert _run(out).skipped == 10

    # --retry-errors: only the errored id is re-evaluated.
    stats = _run(out, retry_errors=True)
    assert stats.skipped == 9
    assert stats.processed == 1
    assert "t003" in _ids(out / "curated.jsonl") + _ids(out / "rejected.jsonl")


@pytest.mark.parametrize("concurrency", [1, 4])
def test_auth_error_fails_fast(tmp_path: Path, concurrency: int):
    out = tmp_path / "out"
    client = _BadKey()
    with pytest.raises(TypeSafeAuthenticationError):
        _run(out, client=client, concurrency=concurrency)
    assert not (out / "errors.jsonl").exists()
    assert client.calls < 10
