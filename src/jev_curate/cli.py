"""CLI for jev-curate."""

from __future__ import annotations

import os
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from typesafe_sdk import TypeSafeAPIError, TypeSafeAuthenticationError, TypeSafeError

from jev_curate.client import make_client
from jev_curate.pipeline import CurationPipeline, PipelineConfig, summarize
from jev_curate.rubric import load_rubric

console = Console()


@click.group()
@click.version_option(package_name="jev-curate")
def main() -> None:
    """Filter training corpora with TypeSafe Jev pass/fail gates."""


@main.command()
@click.option("--rubric", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--input", "input_path", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--output", "output_dir", required=True, type=click.Path(path_type=Path))
@click.option(
    "--mock",
    is_flag=True,
    help="Use mock Jev (tests only). Default: live API when TYPESAFE_API_KEY is set.",
)
@click.option("--limit", type=int, default=None, help="Evaluate at most N rows not already done.")
@click.option(
    "--concurrency",
    type=click.IntRange(min=1),
    default=1,
    show_default=True,
    help="Parallel Jev calls. Respect your TypeSafe rate limit.",
)
@click.option(
    "--retry-errors",
    is_flag=True,
    help="Re-evaluate ids that are only in errors.jsonl instead of skipping them.",
)
def run(
    rubric: Path,
    input_path: Path,
    output_dir: Path,
    mock: bool,
    limit: int | None,
    concurrency: int,
    retry_errors: bool,
) -> None:
    """Run curation gates over JSONL; write curated.jsonl and rejected.jsonl."""
    loaded = load_rubric(rubric)
    live = not mock
    if live and not os.environ.get("TYPESAFE_API_KEY"):
        raise click.ClickException(
            "Live Jev requires TYPESAFE_API_KEY. Export your key or pass --mock for offline tests."
        )

    client = make_client(live=live)
    mode = "live (TypeSafe Jev)" if live else "mock (tests only)"
    console.print(
        f"[bold]jev-curate[/] rubric={loaded.name!r} model={loaded.model} "
        f"mode={mode} concurrency={concurrency}"
    )

    pipeline = CurationPipeline(
        PipelineConfig(
            rubric=loaded,
            input_path=input_path,
            output_dir=output_dir,
            limit=limit,
            concurrency=concurrency,
            retry_errors=retry_errors,
        ),
        client=client,
    )
    try:
        stats = pipeline.run()
    except TypeSafeAuthenticationError as exc:
        raise click.ClickException(f"TypeSafe rejected the API key: {exc}") from exc
    summary = summarize(output_dir)

    table = Table(title="Curation results")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Processed", str(stats.processed))
    table.add_row("Skipped (resume)", str(stats.skipped))
    table.add_row("Kept → curated.jsonl", str(stats.kept))
    table.add_row("Rejected", str(stats.rejected))
    table.add_row("Errors", str(stats.errors))
    table.add_row("Keep rate", f"{summary['keep_rate']:.1%}")
    console.print(table)

    if stats.reject_reasons:
        rt = Table(title="Top reject gates")
        rt.add_column("Gate")
        rt.add_column("Count", justify="right")
        for gate, count in stats.reject_reasons.most_common():
            rt.add_row(gate, str(count))
        console.print(rt)


@main.command()
@click.option("--output", "output_dir", required=True, type=click.Path(exists=True, path_type=Path))
def stats(output_dir: Path) -> None:
    """Summarize a prior curation run."""
    s = summarize(output_dir)
    table = Table(title=str(output_dir))
    for k, v in s.items():
        table.add_row(k, f"{v:.1%}" if k == "keep_rate" else str(v))
    console.print(table)


@main.command("validate-rubric")
@click.option("--rubric", required=True, type=click.Path(exists=True, path_type=Path))
def validate_rubric_cmd(rubric: Path) -> None:
    """Parse rubric YAML and list gates."""
    loaded = load_rubric(rubric)
    table = Table(title=f"Rubric: {loaded.name} (pass_mode={loaded.pass_mode})")
    table.add_column("Gate")
    table.add_column("Type")
    table.add_column("Required")
    for g in loaded.gates:
        table.add_row(g.name, g.kind, "yes" if g.required else "audit-only")
    console.print(table)


@main.command("check-jev")
def check_jev() -> None:
    """Verify TYPESAFE_API_KEY and a minimal live Jev call."""
    from typesafe_sdk import Noul

    try:
        client = make_client(live=True)
        response = client.evaluate(
            state="Hello, this is a connectivity check.",
            questions={"ok": Noul(instructions="This is a coherent English sentence")},
            model="jev-latest",
        )
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
    except TypeSafeAPIError as exc:
        raise click.ClickException(f"Live Jev call failed (HTTP {exc.status}): {exc}") from exc
    except TypeSafeError as exc:
        raise click.ClickException(f"Live Jev call failed: {exc}") from exc
    p = response.answers["ok"].noul  # type: ignore[union-attr]
    console.print(f"Live Jev OK — model={response.model} ok.noul={p:.3f}")
