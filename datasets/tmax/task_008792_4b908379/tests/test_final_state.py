# test_final_state.py

import os
import json
import math

def test_final_output_exists():
    path = "/home/user/final_output.jsonl"
    assert os.path.isfile(path), f"Expected output file not found at {path}."

def test_final_output_content():
    path = "/home/user/final_output.jsonl"

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 4, f"Expected 4 lines in {path}, found {len(lines)}."

    records = []
    for i, line in enumerate(lines):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Line {i+1} is not valid JSON: {line}"

    # Check sorting
    tx_ids = [r.get("tx_id") for r in records]
    assert tx_ids == ["t1", "t2", "t3", "t4"], f"Records are not sorted by tx_id ascending. Found: {tx_ids}"

    # Expected data structure
    expected_names = {
        1: "Alice Böhm",
        2: "Bob Sm[?]th",
        3: "Charlie [?]"
    }

    for r in records:
        tx_id = r.get("tx_id")
        user_id = r.get("user_id")

        # Check required fields
        for field in ["tx_id", "user_id", "amount", "tx_coords", "name", "email", "home_coords", "flagged"]:
            assert field in r, f"Record {tx_id} is missing required field '{field}'."

        # Check email masking
        assert r["email"] == "***@***.***", f"Email for {tx_id} is not properly masked. Found: {r['email']}"

        # Check name cleaning
        expected_name = expected_names.get(user_id)
        assert r["name"] == expected_name, f"Name for {tx_id} (user {user_id}) is incorrect. Expected '{expected_name}', found '{r['name']}'."

        # Check flagged logic
        x1, y1 = r["home_coords"]
        x2, y2 = r["tx_coords"]
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        expected_flag = dist > 10.0

        assert r["flagged"] is expected_flag, f"Flagged status for {tx_id} is incorrect. Dist: {dist}, Expected: {expected_flag}, Found: {r['flagged']}"