# test_final_state.py

import os
import json
import pytest

def test_archive_jsonl_final_state():
    archive_file = "/home/user/backup/archive.jsonl"
    assert os.path.isfile(archive_file), f"File {archive_file} is missing."

    expected_records = [
        {"RecordID": "101", "Date": "2023-11-01", "SensorType": "Temperature", "Value": 15.2},
        {"RecordID": "099", "Date": "2023-10-31", "SensorType": "Humidity", "Value": 50.1},
        {"RecordID": "103", "Date": "2023-11-02", "SensorType": "Humidity", "Value": 45.0},
        {"RecordID": "105", "Date": "2023-11-03", "SensorType": "Radiation", "Value": 12.1},
        {"RecordID": "106", "Date": "2023-11-03", "SensorType": "Temperature", "Value": 22.4}
    ]

    actual_records = []
    with open(archive_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {archive_file} is not valid JSON: {line}")

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} records in {archive_file}, but found {len(actual_records)}. "
        f"Actual records: {actual_records}"
    )

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual == expected, (
            f"Record at line {i+1} does not match expected.\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )

def test_input_files_unmodified():
    criteria_file = "/home/user/dataset/criteria.ini"
    log_file = "/home/user/dataset/instrument.log"

    assert os.path.isfile(criteria_file), "criteria.ini was deleted."
    assert os.path.isfile(log_file), "instrument.log was deleted."

    with open(criteria_file, 'r') as f:
        criteria_content = f.read()
    assert "valid_sensors = Temperature, Humidity, Radiation" in criteria_content, "criteria.ini was modified."
    assert "min_value = 10.5" in criteria_content, "criteria.ini was modified."

    with open(log_file, 'r') as f:
        log_content = f.read()
    assert "RecordID: 101" in log_content and "RecordID: 106" in log_content, "instrument.log was modified."