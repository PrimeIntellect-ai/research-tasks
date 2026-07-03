# test_final_state.py

import os
import json
import pytest

def test_migrated_metrics_json():
    file_path = "/home/user/migrated_metrics.json"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected = [
        {
            "ts": 1600000000,
            "metrics": {
                "cpu": 10.0,
                "mem": 80.1
            },
            "stats": {
                "cpu_sma_3": 10.0,
                "cpu_var_3": 0.0
            }
        },
        {
            "ts": 1600000060,
            "metrics": {
                "cpu": 20.0,
                "mem": 81.0
            },
            "stats": {
                "cpu_sma_3": 15.0,
                "cpu_var_3": 25.0
            }
        },
        {
            "ts": 1600000120,
            "metrics": {
                "cpu": 30.0,
                "mem": 82.5
            },
            "stats": {
                "cpu_sma_3": 20.0,
                "cpu_var_3": 66.6667
            }
        },
        {
            "ts": 1600000180,
            "metrics": {
                "cpu": 20.0,
                "mem": 80.0
            },
            "stats": {
                "cpu_sma_3": 23.3333,
                "cpu_var_3": 22.2222
            }
        },
        {
            "ts": 1600000240,
            "metrics": {
                "cpu": 10.0,
                "mem": 79.5
            },
            "stats": {
                "cpu_sma_3": 20.0,
                "cpu_var_3": 66.6667
            }
        }
    ]

    assert isinstance(data, list), "The JSON output should be a list of objects."
    assert len(data) == len(expected), f"Expected {len(expected)} elements, but got {len(data)}."

    for i, (actual_item, expected_item) in enumerate(zip(data, expected)):
        assert actual_item == expected_item, f"Mismatch at index {i}. Expected {expected_item}, but got {actual_item}."