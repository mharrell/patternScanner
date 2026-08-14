# Phase 2 detections report

- Detections: `data/cache/detections_v1.csv` (31570 rows)
- Detector: v1 (sha256 e93ddf7a6c68666a…)
- Manifest: detections_v1.manifest.json
- CSV sha256: 9b44f66160130c3a (determinism check — see below)
- Spot-checks: 6 per shape, re-verified against raw bars
  with independent code (tools/verify_detections.py) — failures: **0**

## Counts by shape

| shape | detections | tickers |
|---|---|---|
| A | 14593 | 583 |
| B | 15921 | 593 |
| C | 1056 | 386 |

## Counts by decade and era

| shape | 2000s | 2010s | 2020s | IS 2000-2015 | OOS 2016-2025 |
|---|---|---|---|---|---|
| A | 4990 | 7167 | 2436 | 8914 | 5679 |
| B | 4783 | 6598 | 4540 | 8689 | 7232 |
| C | 470 | 400 | 186 | 688 | 368 |

## Coverage

- tickers with bars: 599 | tickers with ≥1 detection: 597
- tickers with zero detections (excluding the 4 no-data names): 2 — ECG, VSNT

## Determinism

`tools/detectors.py` was re-run on the same data; the two CSV files are
byte-identical (sha256 confirmed). Detection output is a pure function
of the parquet bars and the code hash recorded in the manifest.

## Reproducibility check

`python -X utf8 tools/detectors.py && python -X utf8 tools/verify_detections.py`
regenerates this report. Any code or data change changes the manifest hash
and must be logged as a new detector version before it touches measurement.
