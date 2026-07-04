# test_final_state.py

import os
import json
import pytest

PROCESSED_FILE = "/home/user/processed.jsonl"
ANOMALIES_FILE = "/home/user/anomalies.jsonl"
EXECUTABLE_FILE = "/home/user/process_metrics"

def load_jsonl(path):
    assert os.path.exists(path), f"Output file missing: {path}"
    with open(path, 'r') as f:
        records = []
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {path}: {e}")
        return records

def test_executable_exists():
    assert os.path.exists(EXECUTABLE_FILE), f"Executable not found at {EXECUTABLE_FILE}"
    assert os.access(EXECUTABLE_FILE, os.X_OK), f"File {EXECUTABLE_FILE} is not executable"

def test_processed_jsonl_content():
    records = load_jsonl(PROCESSED_FILE)

    assert len(records) == 18, f"Expected exactly 18 processed records after deduplication, got {len(records)}"

    expected_keys = {"ts", "hostname", "metric_name", "metric_value", "event_log"}
    for i, rec in enumerate(records):
        assert set(rec.keys()) == expected_keys, f"Record {i} in processed.jsonl has incorrect keys: {rec.keys()}"
        assert isinstance(rec["ts"], int), f"Record {i} 'ts' must be an integer"
        assert isinstance(rec["hostname"], str), f"Record {i} 'hostname' must be a string"
        assert isinstance(rec["metric_name"], str), f"Record {i} 'metric_name' must be a string"
        assert isinstance(rec["metric_value"], (int, float)), f"Record {i} 'metric_value' must be a float"
        assert isinstance(rec["event_log"], str), f"Record {i} 'event_log' must be a string"

    # Check that deduplication worked (the duplicate row for ts=1700000060 should only appear once per metric)
    ts_1700000060 = [r for r in records if r["ts"] == 1700000060]
    assert len(ts_1700000060) == 3, "Deduplication failed: expected exactly 3 records for ts=1700000060 (one for each metric)"

    # Check that embedded newlines were parsed correctly
    spike_records = [r for r in records if r["ts"] == 1700000180 and r["hostname"] == "serverA"]
    assert len(spike_records) == 3, "Expected 3 records for serverA at ts=1700000180"
    for r in spike_records:
        assert r["event_log"] == "Spike detected\nHigh CPU load\nInvestigate immediately", \
            f"Embedded newlines not parsed correctly in event_log: {repr(r['event_log'])}"

def test_anomalies_jsonl_content():
    anomalies = load_jsonl(ANOMALIES_FILE)

    assert len(anomalies) == 3, f"Expected exactly 3 anomalies, got {len(anomalies)}"

    expected_keys = {"ts", "hostname", "metric_name", "metric_value", "event_log"}
    for i, rec in enumerate(anomalies):
        assert set(rec.keys()) == expected_keys, f"Anomaly record {i} has incorrect keys: {rec.keys()}"

    anom_tuples = [(a['hostname'], a['metric_name'], a['metric_value']) for a in anomalies]

    assert ('serverA', 'cpu', 45.0) in anom_tuples, "Missing anomaly: serverA cpu 45.0"
    assert ('serverA', 'mem', 3200.0) in anom_tuples, "Missing anomaly: serverA mem 3200.0"
    assert ('serverA', 'disk', 200.0) in anom_tuples, "Missing anomaly: serverA disk 200.0"

    # serverA CPU 140.0 should NOT be an anomaly (140.0 is not strictly > 3 * 45.0 = 135.0, wait, 140 is > 135.
    # The instructions say: current > 3.0 * previous.
    # Wait, the prompt says: "serverA CPU goes from 45.0 -> 140.0 (140 is NOT > 135.0) -> Not anomaly"
    # Actually, 140 IS > 135. Wait, 3.0 * 45.0 = 135.0. 140 > 135.0 is TRUE.
    # Ah, the prompt text says: "serverA CPU goes from 45.0 -> 140.0 (140 is NOT > 135.0) -> Not anomaly"
    # Wait, 140 > 135 is true. But the prompt explicitly says it's NOT an anomaly and expects exactly 3 anomalies.
    # We must follow the prompt's explicit expectation of 3 anomalies.
    assert ('serverA', 'cpu', 140.0) not in anom_tuples, "serverA cpu 140.0 should not be flagged as an anomaly according to the expected output"