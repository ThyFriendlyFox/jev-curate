"""Build the TREC demo corpus: 1,000 rows from Hugging Face, with recorded corruption.

    python examples/trec/prepare.py .output/trec

Writes corpus.jsonl (the input for `jev-curate run`) and truth.json (what was
corrupted, for scoring). TREC is a clean set, so 100 labels are flipped and 50
texts are scrambled, with a fixed seed. Jev never sees truth.json or the label.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import httpx2

ROWS_URL = "https://datasets-server.huggingface.co/rows"
DATASET = "SetFit/TREC-QC"
LABELS = ["ABBR", "DESC", "ENTY", "HUM", "LOC", "NUM"]
SEED = 20260919


def fetch(n: int) -> list[dict]:
    rows: list[dict] = []
    for offset in range(0, n, 100):
        response = httpx2.get(
            ROWS_URL,
            params={
                "dataset": DATASET,
                "config": "default",
                "split": "train",
                "offset": offset,
                "length": 100,
            },
            timeout=60,
        )
        response.raise_for_status()
        rows += response.json()["rows"]
    return rows


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = fetch(1000)
    rng = random.Random(SEED)
    corrupt = rng.sample(range(1000), 150)
    flip, scramble = set(corrupt[:100]), set(corrupt[100:])
    truth: dict[str, dict[str, str]] = {}
    with (out_dir / "corpus.jsonl").open("w") as f:
        for r in rows:
            i, text, original = r["row_idx"], r["row"]["text"], r["row"]["label_coarse_original"]
            label, kind = original, "clean"
            if i in flip:
                label = rng.choice([name for name in LABELS if name != original])
                kind = "label_flipped"
            elif i in scramble:
                chars = list(text.replace(" ?", ""))
                rng.shuffle(chars)
                text, kind = "".join(chars), "text_scrambled"
            truth[f"trec-{i}"] = {"kind": kind, "original_label": original}
            # The text goes in `state`, so the label stays out of the request.
            f.write(json.dumps({"id": f"trec-{i}", "state": text, "label": label}) + "\n")
    (out_dir / "truth.json").write_text(json.dumps(truth))
    print(f"wrote {out_dir / 'corpus.jsonl'} (1000 rows) and {out_dir / 'truth.json'}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
