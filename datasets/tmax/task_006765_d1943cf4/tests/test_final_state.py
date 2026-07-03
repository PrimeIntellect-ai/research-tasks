# test_final_state.py

import os
import json
import pytest

def test_fraud_report_exists_and_valid():
    report_path = '/home/user/fraud_report.json'

    assert os.path.exists(report_path), f"The output file {report_path} was not found."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "ring_participants" in data, "The JSON output is missing the 'ring_participants' key."
    assert "mastermind" in data, "The JSON output is missing the 'mastermind' key."

    expected_participants = [
        "http://example.org/fraud/ACC_001",
        "http://example.org/fraud/ACC_002",
        "http://example.org/fraud/ACC_003",
        "http://example.org/fraud/ACC_004",
        "http://example.org/fraud/ACC_005"
    ]

    actual_participants = data["ring_participants"]
    assert isinstance(actual_participants, list), "'ring_participants' must be a list."
    assert sorted(actual_participants) == sorted(expected_participants), (
        f"Expected ring_participants to be {expected_participants}, but got {actual_participants}."
    )

    # The specification requires the list to be sorted alphabetically
    assert actual_participants == sorted(actual_participants), "'ring_participants' list is not sorted alphabetically."

    expected_mastermind = "http://example.org/fraud/ACC_001"
    actual_mastermind = data["mastermind"]
    assert actual_mastermind == expected_mastermind, (
        f"Expected mastermind to be '{expected_mastermind}', but got '{actual_mastermind}'."
    )

def test_analyze_script_exists():
    script_path = '/home/user/analyze_graph.py'
    assert os.path.exists(script_path), f"The script {script_path} was not found."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."