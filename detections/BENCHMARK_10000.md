# 10,000-Event Detection Benchmark

## Results

- **Events processed:** 10,000
- **Alerts generated:** 10
- **Processing time:** 0.040825 seconds
- **Throughput:** 244,948.21 events/second
- **Detection:** Encoded PowerShell
- **Processing model:** Streaming JSONL ingestion

## Test Design

The benchmark dataset contains 10,000 synthetic Windows process-creation events.

A suspicious encoded PowerShell event is injected once every 1,000 events, producing 10 expected detections.

The ingestion layer processes events incrementally rather than loading the entire dataset into memory.

## Validation

Expected:
- 10,000 events processed
- 10 encoded PowerShell alerts

Observed:
- 10,000 events processed
- 10 alerts generated

## Next Scale Target

The platform will next be tested against larger event sets, with 100,000 events as the stretch benchmark once broader detection execution and correlation are integrated.
