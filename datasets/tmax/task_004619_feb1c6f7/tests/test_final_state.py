# test_final_state.py
import os
import json
import pytest

SCRIPT_PATH = '/home/user/analyze_graph.py'
JSON_PATH = '/home/user/cycles.json'

def test_script_exists_and_parameterized():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    # Check for parameterization signs in the script (e.g., ?, :name, %s)
    has_param = '?' in content or '%s' in content or ':' in content
    assert has_param, "Script does not appear to use parameterized SQL queries."

def test_cycles_json_content():
    assert os.path.exists(JSON_PATH), f"Output JSON missing at {JSON_PATH}"
    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("cycles.json is not valid JSON")

    expected_data = [
        ["AuthService", "UserService", "EmailService"],
        ["PaymentService", "LedgerService", "AuditService"]
    ]

    assert isinstance(data, list), "Output should be a JSON array of lists."
    assert len(data) == 2, f"Expected 2 cycles, found {len(data)}."

    assert data == expected_data, f"Output JSON data does not match expected sorted output. Got: {data}"