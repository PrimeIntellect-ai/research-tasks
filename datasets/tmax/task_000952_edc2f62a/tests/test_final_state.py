# test_final_state.py
import os
import json
import pytest

def test_recovery_report_exists_and_valid():
    report_path = '/home/user/recovery_report.json'
    assert os.path.exists(report_path), f"Output file {report_path} is missing."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    assert isinstance(data, dict), f"Expected the root of {report_path} to be a JSON object."

def test_recovery_report_content():
    report_path = '/home/user/recovery_report.json'
    if not os.path.exists(report_path):
        pytest.fail(f"Cannot test content because {report_path} is missing.")

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON.")

    expected = {
        "101": {"total_amount": 350.5, "transaction_count": 3},
        "105": {"total_amount": 510.0, "transaction_count": 2},
        "204": {"total_amount": 30.0, "transaction_count": 1},
        "300": {"total_amount": 0.0, "transaction_count": 0}
    }

    for user_id, stats in expected.items():
        assert user_id in data, f"Missing user_id '{user_id}' in the recovery report."
        user_data = data[user_id]

        assert "total_amount" in user_data, f"Missing 'total_amount' for user {user_id}."
        assert "transaction_count" in user_data, f"Missing 'transaction_count' for user {user_id}."

        assert isinstance(user_data["transaction_count"], int), f"'transaction_count' for user {user_id} must be an integer."
        assert isinstance(user_data["total_amount"], (int, float)), f"'total_amount' for user {user_id} must be a number."

        assert abs(user_data["total_amount"] - stats["total_amount"]) < 0.01, \
            f"Incorrect 'total_amount' for user {user_id}. Expected {stats['total_amount']}, got {user_data['total_amount']}."
        assert user_data["transaction_count"] == stats["transaction_count"], \
            f"Incorrect 'transaction_count' for user {user_id}. Expected {stats['transaction_count']}, got {user_data['transaction_count']}."

def test_script_uses_not_indexed():
    script_path = '/home/user/recover_data.py'
    assert os.path.exists(script_path), f"Python script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read().upper()

    assert "NOT INDEXED" in content, "The script does not contain the required 'NOT INDEXED' clause to bypass corrupted indices."