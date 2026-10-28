import json
from pathlib import Path

from ingestion.benchmark_detection import benchmark
from ingestion.jsonl_stream import count_events, stream_jsonl


def test_stream_jsonl_reads_events(tmp_path) -> None:
    log_file = tmp_path / "events.jsonl"
    log_file.write_text(
        '{"EventID": 1}\n{"EventID": 2}\n',
        encoding="utf-8",
    )

    events = list(stream_jsonl(log_file))

    assert len(events) == 2
    assert events[0]["EventID"] == 1
    assert events[1]["EventID"] == 2


def test_count_events_returns_correct_total(tmp_path) -> None:
    log_file = tmp_path / "events.jsonl"
    log_file.write_text(
        '{"EventID": 1}\n{"EventID": 1}\n{"EventID": 1}\n',
        encoding="utf-8",
    )

    assert count_events(log_file) == 3


def test_stream_jsonl_rejects_invalid_json(tmp_path) -> None:
    log_file = tmp_path / "bad.jsonl"
    log_file.write_text(
        '{"EventID": 1}\nnot-json\n',
        encoding="utf-8",
    )

    try:
        list(stream_jsonl(log_file))
    except ValueError as error:
        assert "Invalid JSON on line 2" in str(error)
    else:
        raise AssertionError("Expected invalid JSON to raise ValueError")


def test_benchmark_detects_encoded_powershell(tmp_path) -> None:
    log_file = tmp_path / "benchmark.jsonl"

    events = [
        {
            "EventID": 1,
            "Image": r"C:\Windows\System32\notepad.exe",
            "CommandLine": "notepad.exe notes.txt",
        },
        {
            "EventID": 1,
            "Image": (
                r"C:\Windows\System32\WindowsPowerShell"
                r"\v1.0\powershell.exe"
            ),
            "CommandLine": (
                "powershell.exe -EncodedCommand TEST"
            ),
        },
    ]

    with log_file.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    result = benchmark(log_file)

    assert result["events_processed"] == 2
    assert result["alerts_generated"] == 1
    assert result["events_per_second"] > 0
