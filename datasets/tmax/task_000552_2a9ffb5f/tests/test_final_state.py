# test_final_state.py

import os
import json
import csv
import pytest

def test_pipeline_scripts_exist_and_executable():
    run_script = "/home/user/factory_data/run_pipeline.sh"
    extract_script = "/home/user/factory_data/extract.py"
    process_script = "/home/user/factory_data/process.py"

    assert os.path.isfile(run_script), f"{run_script} is missing"
    assert os.access(run_script, os.X_OK), f"{run_script} is not executable"

    assert os.path.isfile(extract_script), f"{extract_script} is missing"
    assert os.path.isfile(process_script), f"{process_script} is missing"

def test_extracted_logs_csv_correctness():
    csv_file = "/home/user/factory_data/extracted_logs.csv"
    assert os.path.isfile(csv_file), f"{csv_file} is missing"

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == ["timestamp", "machine_id", "error_code", "downtime_minutes"], \
        "extracted_logs.csv does not have the correct header"

    expected_rows = [
        {"timestamp": "2023-11-01 10:15:00", "machine_id": "Mach-101", "error_code": "E12", "downtime_minutes": "45"},
        {"timestamp": "2023-11-01 14:30:00", "machine_id": "Mach-204", "error_code": "E99", "downtime_minutes": "120"},
        {"timestamp": "2023-11-02 09:00:00", "machine_id": "Mach-101", "error_code": "E01", "downtime_minutes": "30"},
        {"timestamp": "2023-11-02 11:00:00", "machine_id": "Mach-300", "error_code": "E44", "downtime_minutes": "60"},
    ]

    assert len(rows) == len(expected_rows), "extracted_logs.csv row count mismatch"
    for i, (row, expected) in enumerate(zip(rows, expected_rows)):
        assert row == expected, f"extracted_logs.csv row {i} mismatch. Expected {expected}, got {row}"

def test_final_metrics_jsonl_correctness():
    jsonl_file = "/home/user/factory_data/final_metrics.jsonl"
    assert os.path.isfile(jsonl_file), f"{jsonl_file} is missing"

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    expected_data = [
        {"event_timestamp": "2023-11-01 10:15:00", "machine_id": "Mach-101", "error_code": "E12", "downtime_minutes": 45, "avg_temperature": 47.83, "avg_vibration": 0.5},
        {"event_timestamp": "2023-11-01 14:30:00", "machine_id": "Mach-204", "error_code": "E99", "downtime_minutes": 120, "avg_temperature": 62.33, "avg_vibration": 1.27},
        {"event_timestamp": "2023-11-02 09:00:00", "machine_id": "Mach-101", "error_code": "E01", "downtime_minutes": 30, "avg_temperature": 44.5, "avg_vibration": 0.18},
        {"event_timestamp": "2023-11-02 11:00:00", "machine_id": "Mach-300", "error_code": "E44", "downtime_minutes": 60, "avg_temperature": None, "avg_vibration": None}
    ]

    assert len(lines) == len(expected_data), "final_metrics.jsonl row count mismatch"

    for i, (line, expected) in enumerate(zip(lines, expected_data)):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i} in final_metrics.jsonl is not valid JSON")

        # Check keys
        expected_keys = {"event_timestamp", "machine_id", "error_code", "downtime_minutes", "avg_temperature", "avg_vibration"}
        assert set(parsed.keys()) == expected_keys, f"Line {i} keys mismatch. Expected {expected_keys}, got {set(parsed.keys())}"

        # Check values
        assert parsed["event_timestamp"] == expected["event_timestamp"], f"Line {i} event_timestamp mismatch"
        assert parsed["machine_id"] == expected["machine_id"], f"Line {i} machine_id mismatch"
        assert parsed["error_code"] == expected["error_code"], f"Line {i} error_code mismatch"
        assert parsed["downtime_minutes"] == expected["downtime_minutes"], f"Line {i} downtime_minutes mismatch"

        if expected["avg_temperature"] is None:
            assert parsed["avg_temperature"] is None, f"Line {i} avg_temperature should be null"
        else:
            assert abs(parsed["avg_temperature"] - expected["avg_temperature"]) < 0.01, f"Line {i} avg_temperature mismatch"

        if expected["avg_vibration"] is None:
            assert parsed["avg_vibration"] is None, f"Line {i} avg_vibration should be null"
        else:
            assert abs(parsed["avg_vibration"] - expected["avg_vibration"]) < 0.01, f"Line {i} avg_vibration mismatch"