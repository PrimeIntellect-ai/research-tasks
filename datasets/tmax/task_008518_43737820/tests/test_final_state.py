# test_final_state.py
import os
import json
import math

def test_output_file_exists():
    output_path = "/home/user/user_spend.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did the script run successfully?"

def test_output_file_content_and_schema():
    output_path = "/home/user/user_spend.jsonl"
    if not os.path.isfile(output_path):
        return # Handled by previous test

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in the output file, but got {len(lines)}."

    parsed_lines = []
    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            parsed_lines.append(data)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} is not valid JSON: {line}"

    # Check sorting
    user_ids = [row.get("user_id") for row in parsed_lines]
    assert user_ids == sorted(user_ids), "The output file is not sorted alphabetically by user_id."

    # Expected data mapping
    expected_data = {
        "u1": {
            "email": "alice@example.com",
            "total_spent": 1231.5,
            "order_count": 2,
            "top_category": "electronics"
        },
        "u2": {
            "email": "bob@example.com",
            "total_spent": 75.0,
            "order_count": 1,
            "top_category": "electronics"
        },
        "u3": {
            "email": "charlie@example.com",
            "total_spent": 400.0,
            "order_count": 2,
            "top_category": "furniture"
        }
    }

    for row in parsed_lines:
        uid = row.get("user_id")
        assert uid in expected_data, f"Unexpected user_id found: {uid}"

        expected = expected_data[uid]
        assert row.get("email") == expected["email"], f"Incorrect email for user {uid}"
        assert row.get("order_count") == expected["order_count"], f"Incorrect order_count for user {uid}"
        assert row.get("top_category") == expected["top_category"], f"Incorrect top_category for user {uid}"

        actual_spent = row.get("total_spent")
        assert isinstance(actual_spent, (int, float)), f"total_spent for user {uid} must be a number"
        assert math.isclose(actual_spent, expected["total_spent"], rel_tol=1e-5), f"Incorrect total_spent for user {uid}: expected {expected['total_spent']}, got {actual_spent}"