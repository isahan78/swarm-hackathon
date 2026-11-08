"""Strict, interoperable JSONL without pickle or implicit outcome enrichment."""
import json
from pathlib import Path


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")


def read_jsonl(path):
    rows = []
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Invalid JSON at {path}:{line_number}") from error
                if not isinstance(row, dict):
                    raise ValueError(f"Expected object at {path}:{line_number}")
                rows.append(row)
    return rows


def append_jsonl(path, rows):
    """Append one complete episode to an already-created journal (single writer)."""
    with Path(path).open("a", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
        stream.flush()
