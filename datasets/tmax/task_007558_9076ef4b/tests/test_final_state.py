# test_final_state.py
import os
import json
import pytest

def test_structured_runs_jsonl_exists_and_content():
    output_path = "/home/user/structured_runs.jsonl"

    assert os.path.exists(output_path), f"Expected output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

    expected_data = [
        {
            "Timestamp": "2023-10-01T12:00:00Z",
            "RunID": "1042",
            "User": "USER_ANONYMIZED",
            "Parameters": "alpha=0.5\nbeta=1.2\ngamma=3.0",
            "Results": "SUCCESS"
        },
        {
            "Timestamp": "2023-10-02T14:30:00Z",
            "RunID": "1043",
            "User": "USER_ANONYMIZED",
            "Parameters": "model=transformer\nlayers=12",
            "Results": "FAILURE"
        },
        {
            "Timestamp": "2023-10-03T09:15:00Z",
            "RunID": "1044",
            "User": "USER_ANONYMIZED",
            "Parameters": "",
            "Results": "SUCCESS"
        }
    ]

    actual_data = []
    with open(output_path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_data.append(record)
            except json.JSONDecodeError as e:
                pytest.fail(f"Line {line_num} in {output_path} is not valid JSON: {e}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, but found {len(actual_data)} in {output_path}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Record at index {i} does not match expected output.\nExpected: {expected}\nActual: {actual}"