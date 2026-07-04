# test_final_state.py
import os
import pytest

def test_escalation_audit_csv_exists():
    csv_path = "/home/user/escalation_audit.csv"
    assert os.path.isfile(csv_path), f"The audit report {csv_path} does not exist."

def test_escalation_audit_csv_content():
    csv_path = "/home/user/escalation_audit.csv"
    assert os.path.isfile(csv_path), f"The audit report {csv_path} does not exist."

    with open(csv_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "Username,UID,WorldWritable",
        "bob,1002,true",
        "dave,1004,true",
        "eve,1005,false"
    ]

    assert len(content) > 0, "The CSV file is empty."
    assert content[0] == expected_content[0], f"CSV header is incorrect. Expected '{expected_content[0]}', got '{content[0]}'."

    # Check if lines match exactly
    assert len(content) == len(expected_content), f"Expected {len(expected_content)} lines, but got {len(content)}."

    for i in range(1, len(expected_content)):
        assert content[i] == expected_content[i], f"Line {i+1} is incorrect. Expected '{expected_content[i]}', got '{content[i]}'."