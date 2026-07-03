# test_final_state.py

import os
import json
import sys
import subprocess
import pytest

def test_minimized_transactions():
    """Verify minimized_transactions.json contains exactly the crashing transaction."""
    file_path = "/home/user/minimized_transactions.json"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not valid JSON.")

    assert isinstance(data, list), "minimized_transactions.json must contain a JSON array."
    assert len(data) == 1, f"Expected exactly 1 transaction, found {len(data)}."

    tx = data[0]
    assert tx.get("date") == "2023-10-31", "The minimized transaction must be the one on '2023-10-31'."
    assert tx.get("id") == "tx005", "The minimized transaction must have id 'tx005'."
    assert tx.get("amount") == 25.0, "The minimized transaction must have amount 25.0."

def test_billing_processor_fixed():
    """Verify the off-by-one error in billing_processor.py is fixed."""
    sys.path.insert(0, "/home/user")
    try:
        import billing_processor
    except ImportError:
        pytest.fail("Could not import billing_processor.py from /home/user")

    assert hasattr(billing_processor, 'calculate_daily_aggregates'), "calculate_daily_aggregates missing."

    # Test the fixed function
    res = billing_processor.calculate_daily_aggregates([], '2023-10-01', '2023-10-31')
    assert len(res) == 31, f"Expected 31 elements for inclusive range Oct 1 to Oct 31, got {len(res)}."

def test_regression_test_exists_and_passes():
    """Verify test_billing.py exists, contains the required test, and passes."""
    file_path = "/home/user/test_billing.py"
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read()
        assert "def test_end_date_inclusive" in content, "test_end_date_inclusive() function missing in test_billing.py"

    result = subprocess.run(["pytest", file_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest on {file_path} failed:\n{result.stdout}\n{result.stderr}"