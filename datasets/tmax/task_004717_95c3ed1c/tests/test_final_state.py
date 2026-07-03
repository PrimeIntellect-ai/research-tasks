# test_final_state.py

import os
import json
import pytest

def test_cycles_report_exists_and_correct():
    report_path = "/home/user/output/cycles_report.json"
    assert os.path.isfile(report_path), f"Expected output file is missing: {report_path}"

    with open(report_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    expected_data = [
        {
            "cycle": ["P04", "P05", "P06"],
            "max_score": 91
        },
        {
            "cycle": ["P01", "P02", "P03"],
            "max_score": 62
        },
        {
            "cycle": ["P07", "P08"],
            "max_score": 40
        }
    ]

    assert isinstance(actual_data, list), "Output JSON should be a list of objects."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} cycles, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert "cycle" in actual, f"Object at index {i} missing 'cycle' key."
        assert "max_score" in actual, f"Object at index {i} missing 'max_score' key."

        # Ensure the cycle array is sorted lexicographically as required
        assert actual["cycle"] == sorted(actual["cycle"]), f"Cycle at index {i} is not sorted lexicographically."

        assert actual["cycle"] == expected["cycle"], f"Cycle at index {i} mismatch. Expected {expected['cycle']}, got {actual['cycle']}."
        assert actual["max_score"] == expected["max_score"], f"max_score at index {i} mismatch. Expected {expected['max_score']}, got {actual['max_score']}."