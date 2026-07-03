# test_final_state.py

import os
import csv
import json
import math
import pytest

def get_expected_data():
    users_path = "/home/user/users.csv"
    tx_path = "/home/user/transactions.csv"

    assert os.path.isfile(users_path), f"Missing {users_path}"
    assert os.path.isfile(tx_path), f"Missing {tx_path}"

    users = {}
    with open(users_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row["user_id"]
            users[uid] = {
                "user_id": uid,
                "name": row["name"],
                "total_spent": 0.0,
                "max_transaction": 0.0
            }

    with open(tx_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row["user_id"]
            if uid in users:
                amount = float(row["amount"])
                users[uid]["total_spent"] += amount
                if amount > users[uid]["max_transaction"]:
                    users[uid]["max_transaction"] = amount

    # Sort by user_id
    sorted_users = sorted(users.values(), key=lambda x: x["user_id"])
    return sorted_users

def test_output_json_exists_and_correct():
    out_path = "/home/user/output.json"
    assert os.path.isfile(out_path), f"Output file {out_path} was not created."

    with open(out_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {out_path} is not valid JSON.")

    assert isinstance(data, list), f"Expected a JSON array in {out_path}, but got {type(data).__name__}."

    expected_data = get_expected_data()

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in output JSON, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert "user_id" in actual, f"Item at index {i} missing 'user_id'"
        assert "name" in actual, f"Item at index {i} missing 'name'"
        assert "total_spent" in actual, f"Item at index {i} missing 'total_spent'"
        assert "max_transaction" in actual, f"Item at index {i} missing 'max_transaction'"

        assert actual["user_id"] == expected["user_id"], f"Expected user_id '{expected['user_id']}' at index {i}, got '{actual['user_id']}'. (Ensure the array is sorted by user_id)"
        assert actual["name"] == expected["name"], f"Expected name '{expected['name']}' for user_id '{expected['user_id']}', got '{actual['name']}'"

        actual_total = float(actual["total_spent"])
        expected_total = expected["total_spent"]
        assert math.isclose(actual_total, expected_total, rel_tol=1e-5, abs_tol=1e-2), \
            f"Expected total_spent {expected_total} for user {expected['user_id']}, got {actual_total}"

        actual_max = float(actual["max_transaction"])
        expected_max = expected["max_transaction"]
        assert math.isclose(actual_max, expected_max, rel_tol=1e-5, abs_tol=1e-2), \
            f"Expected max_transaction {expected_max} for user {expected['user_id']}, got {actual_max}"