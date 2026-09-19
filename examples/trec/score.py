"""Score a TREC demo run against the recorded corruption.

python examples/trec/score.py .output/trec .output/trec/run1
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def main(data_dir: Path, run_dir: Path) -> None:
    truth = json.loads((data_dir / "truth.json").read_text())
    verdicts = {
        name: [json.loads(line) for line in (run_dir / f"{name}.jsonl").read_text().splitlines()]
        for name in ("curated", "rejected")
    }
    kept, rejected = verdicts["curated"], verdicts["rejected"]
    print(f"evaluated {len(kept) + len(rejected)}: kept {len(kept)}, rejected {len(rejected)}")
    counts = Counter(
        (truth[r["id"]]["kind"], name) for name, rows in verdicts.items() for r in rows
    )
    for kind in ("label_flipped", "text_scrambled", "clean"):
        n_rejected, n_kept = counts[(kind, "rejected")], counts[(kind, "curated")]
        if n_rejected + n_kept:
            share = n_rejected / (n_rejected + n_kept)
            print(f"  {kind:15} rejected {n_rejected:4} of {n_rejected + n_kept:4} ({share:.0%})")
    restored = sum(
        1
        for r in rejected
        if truth[r["id"]]["kind"] == "label_flipped"
        and r["_curation"]["gates"]["label_matches"]["answer"]["choice"]
        == truth[r["id"]]["original_label"]
    )
    print(f"  flipped rows where Jev chose the original label: {restored}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
