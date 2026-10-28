import argparse
import json
import time
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from automation.detect_encoded_powershell import (
    is_encoded_powershell,
)
from ingestion.jsonl_stream import stream_jsonl


def benchmark(path: Path) -> dict:
    start = time.perf_counter()

    total_events = 0
    alerts = 0

    for event in stream_jsonl(path):
        total_events += 1

        if is_encoded_powershell(event):
            alerts += 1

    elapsed = time.perf_counter() - start

    events_per_second = (
        total_events / elapsed
        if elapsed > 0
        else 0
    )

    return {
        "input_file": str(path),
        "events_processed": total_events,
        "alerts_generated": alerts,
        "processing_seconds": round(elapsed, 6),
        "events_per_second": round(
            events_per_second,
            2,
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "sample-logs/benchmark_10000.jsonl"
        ),
    )

    args = parser.parse_args()
    result = benchmark(args.input)

    output = Path(
        "detections/benchmark_10000_results.json"
    )

    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
