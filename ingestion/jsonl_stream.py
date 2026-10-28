import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def stream_jsonl(path: str | Path) -> Iterator[dict[str, Any]]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Log file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                yield json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {error}"
                ) from error


def count_events(path: str | Path) -> int:
    return sum(1 for _ in stream_jsonl(path))
