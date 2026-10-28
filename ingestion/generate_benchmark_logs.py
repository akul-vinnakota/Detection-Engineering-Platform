import argparse
import json
from pathlib import Path


def generate_events(count: int, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        for index in range(count):
            event = {
                "EventID": 1,
                "Computer": f"LAB-WIN{index % 25:02d}",
                "User": f"LAB\\user{index % 100}",
                "Image": r"C:\Windows\System32\notepad.exe",
                "CommandLine": f"notepad.exe document-{index}.txt",
            }

            # Inject a suspicious encoded PowerShell event
            # every 1,000 events.
            if index % 1000 == 0:
                event = {
                    "EventID": 1,
                    "Computer": f"LAB-WIN{index % 25:02d}",
                    "User": f"LAB\\user{index % 100}",
                    "Image": (
                        r"C:\Windows\System32\WindowsPowerShell"
                        r"\v1.0\powershell.exe"
                    ),
                    "CommandLine": (
                        "powershell.exe -EncodedCommand "
                        "VwByAGkAdABlAC0ASABvAHMAdAA="
                    ),
                }

            file.write(json.dumps(event) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count",
        type=int,
        default=10000,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("sample-logs/benchmark_10000.jsonl"),
    )

    args = parser.parse_args()

    generate_events(args.count, args.output)

    print(f"Generated events: {args.count}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
