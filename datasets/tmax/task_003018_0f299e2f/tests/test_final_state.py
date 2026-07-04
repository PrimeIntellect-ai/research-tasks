# test_final_state.py
import os
import json
import re
import pytest

def test_anomalies_json():
    """Verify that anomalies.json is correctly generated with expected anomalies."""
    path = "/home/user/anomalies.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run your script and generate the report?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file.")

    assert "missing_tx_ids" in data, "Key 'missing_tx_ids' is missing from anomalies.json"
    assert "invalid_doc_user_ids" in data, "Key 'invalid_doc_user_ids' is missing from anomalies.json"

    expected_missing_tx_ids = ["tx104", "tx105"]
    expected_invalid_doc_user_ids = [3, 4, 5]

    assert data["missing_tx_ids"] == expected_missing_tx_ids, \
        f"Expected missing_tx_ids to be {expected_missing_tx_ids}, but got {data['missing_tx_ids']}"

    assert data["invalid_doc_user_ids"] == expected_invalid_doc_user_ids, \
        f"Expected invalid_doc_user_ids to be {expected_invalid_doc_user_ids}, but got {data['invalid_doc_user_ids']}"

def test_index_strategy_sql():
    """Verify that index_strategy.sql contains the correct CREATE INDEX statement."""
    path = "/home/user/index_strategy.sql"
    assert os.path.isfile(path), f"File {path} does not exist. Did you create the SQL file?"

    with open(path, "r") as f:
        content = f.read().strip().lower()

    # Check for basic SQL keywords and names
    assert "create " in content and "index " in content, "The file must contain a CREATE INDEX statement."
    assert "idx_tx_user_status_created" in content, "The index must be named 'idx_tx_user_status_created'."
    assert "on transactions" in content or "on `transactions`" in content or 'on "transactions"' in content, \
        "The index must be created on the 'transactions' table."

    # Extract the columns part inside parentheses
    match = re.search(r'\(([^)]+)\)', content)
    assert match, "Could not find the column list in parentheses for the CREATE INDEX statement."

    columns_str = match.group(1)
    # Clean up the columns string
    cols = [c.strip().split()[0] for c in columns_str.split(',')]
    cols = [c.replace('`', '').replace('"', '') for c in cols]

    assert "user_id" in cols, "The index must include the 'user_id' column."
    assert "status" in cols, "The index must include the 'status' column."
    assert "created_at" in cols, "The index must include the 'created_at' column."

    # Check for the correct order (user_id, status, created_at)
    # Order is important for the query: WHERE user_id = ? AND status = ? ORDER BY created_at DESC
    # (user_id, status) can be swapped, but created_at must be last.
    assert cols[-1] == "created_at", "The 'created_at' column must be the last column in the index for optimal sorting."
    assert set(cols[:2]) == {"user_id", "status"}, "The first two columns in the index must be 'user_id' and 'status'."