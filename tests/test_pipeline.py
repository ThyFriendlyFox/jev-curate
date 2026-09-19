from pathlib import Path

from jev_curate.client import make_client
from jev_curate.pipeline import CurationPipeline, PipelineConfig, summarize
from jev_curate.rubric import load_rubric


def test_pipeline_mock(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    rubric = load_rubric(root / "examples" / "training-cleanup" / "rubric.yaml")
    inp = root / "examples" / "training-cleanup" / "corpus.jsonl"
    out = tmp_path / "out"
    pipeline = CurationPipeline(
        PipelineConfig(rubric=rubric, input_path=inp, output_dir=out),
        client=make_client(live=False),
    )
    stats = pipeline.run()
    assert stats.processed == 10
    s = summarize(out)
    assert s["curated"] + s["rejected"] == 10
    assert (out / "audit.jsonl").exists()
