from pathlib import Path

from click.testing import CliRunner

from jev_curate.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_run_without_key_fails():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "run",
            "--rubric",
            str(ROOT / "examples/rubric.yaml"),
            "--input",
            str(ROOT / "examples/corpus.jsonl"),
            "--output",
            "out",
        ],
        env={"TYPESAFE_API_KEY": ""},
    )
    assert result.exit_code != 0
    assert "TYPESAFE_API_KEY" in result.output


def test_run_mock_writes_outputs(tmp_path: Path):
    runner = CliRunner()
    out = tmp_path / "out"
    result = runner.invoke(
        main,
        [
            "run",
            "--mock",
            "--rubric",
            str(ROOT / "examples/rubric.yaml"),
            "--input",
            str(ROOT / "examples/corpus.jsonl"),
            "--output",
            str(out),
            "--concurrency",
            "2",
        ],
    )
    assert result.exit_code == 0, result.output
    for name in ("curated", "rejected", "audit"):
        assert (out / f"{name}.jsonl").exists()
    assert runner.invoke(main, ["stats", "--output", str(out)]).exit_code == 0


def test_validate_rubric():
    result = CliRunner().invoke(
        main, ["validate-rubric", "--rubric", str(ROOT / "examples/rubric.yaml")]
    )
    assert result.exit_code == 0, result.output
    assert "bucket_matches_content" in result.output


def test_check_jev_without_key_fails_plainly():
    result = CliRunner().invoke(main, ["check-jev"], env={"TYPESAFE_API_KEY": ""})
    assert result.exit_code != 0
    assert "TYPESAFE_API_KEY" in result.output
    assert "Traceback" not in result.output
