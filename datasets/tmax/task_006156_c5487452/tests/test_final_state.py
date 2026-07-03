# test_final_state.py

import os
import json
import pytest

def test_mre_txt_content():
    path = "/home/user/mre.txt"
    assert os.path.isfile(path), f"File {path} is missing. You need to create it with the isolated input."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_line = "TXN_003,1000.0,0.1;0.1;0.1,0.3"
    assert content == expected_line, f"Content of {path} is incorrect. Expected exactly the line causing the crash."

def test_aggregate_py_fixed():
    path = "/home/user/aggregate.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    # Check that 1e-9 is used in the script
    assert "1e-9" in content or "0.000000001" in content, f"The script {path} does not seem to use the 1e-9 threshold as requested."
    assert "abs(" in content, f"The script {path} does not seem to use absolute value for the threshold check."

def test_report_json_generated_and_correct():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the fixed script?"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_data = {
        "TXN_001": 7500.0,
        "TXN_002": "SKIPPED_ZERO",
        "TXN_003": "SKIPPED_ZERO",
        "TXN_004": 6000.0
    }

    assert data == expected_data, f"Content of {path} does not match the expected results."

def test_transactions_wal_unmodified():
    path = "/home/user/transactions.wal"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_content = """TXN_001,1500.0,0.5;0.5,0.8
TXN_002,2000.0,0.5;0.5,1.0
TXN_003,1000.0,0.1;0.1;0.1,0.3
TXN_004,3000.0,0.2;0.4,0.1"""

    assert content == expected_content, f"File {path} was modified, which violates the constraints."