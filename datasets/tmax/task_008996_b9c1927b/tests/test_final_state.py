# test_final_state.py

import os
import json

def test_rolling_stats_json_exists_and_correct():
    file_path = "/home/user/rolling_stats.json"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    assert isinstance(data, list), f"Expected the JSON in {file_path} to be a list, but got {type(data).__name__}."

    expected_data = [
        {
            "window_start": "2023-10-01T10:00:00Z",
            "region": "eu-west-1",
            "total_logs": 1,
            "error_count": 0,
            "rolling_3h_error_avg": 0.0
        },
        {
            "window_start": "2023-10-01T11:00:00Z",
            "region": "eu-west-1",
            "total_logs": 1,
            "error_count": 1,
            "rolling_3h_error_avg": 0.33
        },
        {
            "window_start": "2023-10-01T08:00:00Z",
            "region": "us-east-1",
            "total_logs": 1,
            "error_count": 0,
            "rolling_3h_error_avg": 0.0
        },
        {
            "window_start": "2023-10-01T09:00:00Z",
            "region": "us-east-1",
            "total_logs": 1,
            "error_count": 1,
            "rolling_3h_error_avg": 0.33
        },
        {
            "window_start": "2023-10-01T10:00:00Z",
            "region": "us-east-1",
            "total_logs": 2,
            "error_count": 2,
            "rolling_3h_error_avg": 1.0
        },
        {
            "window_start": "2023-10-01T11:00:00Z",
            "region": "us-east-1",
            "total_logs": 1,
            "error_count": 1,
            "rolling_3h_error_avg": 1.33
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        # Check keys
        expected_keys = set(expected.keys())
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Record {i} keys mismatch. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual["window_start"] == expected["window_start"], f"Record {i} window_start mismatch. Expected {expected['window_start']}, got {actual['window_start']}."
        assert actual["region"] == expected["region"], f"Record {i} region mismatch. Expected {expected['region']}, got {actual['region']}."
        assert actual["total_logs"] == expected["total_logs"], f"Record {i} total_logs mismatch. Expected {expected['total_logs']}, got {actual['total_logs']}."
        assert actual["error_count"] == expected["error_count"], f"Record {i} error_count mismatch. Expected {expected['error_count']}, got {actual['error_count']}."

        # Check rolling average with a small tolerance for float issues, though strict equality is expected per instructions
        assert abs(actual["rolling_3h_error_avg"] - expected["rolling_3h_error_avg"]) < 0.001, \
            f"Record {i} rolling_3h_error_avg mismatch. Expected {expected['rolling_3h_error_avg']}, got {actual['rolling_3h_error_avg']}."