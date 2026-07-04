# test_final_state.py
import os
import csv
import json
import pytest

def get_expected_output():
    """Derive the expected output directly from the input CSV files."""
    users = {}
    with open('/home/user/users.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[int(row['user_id'])] = row['name']

    out_degrees = {u: 0 for u in users}
    with open('/home/user/friends.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = int(row['source_id'])
            out_degrees[src] = out_degrees.get(src, 0) + 1

    max_amounts = {u: 0.0 for u in users}
    with open('/home/user/transactions.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = int(row['user_id'])
            amt = float(row['amount'])
            if amt > max_amounts.get(uid, 0.0):
                max_amounts[uid] = amt

    results = []
    for uid, name in users.items():
        max_amt = max_amounts[uid]
        if max_amt > 50.0:
            results.append({
                "user_id": uid,
                "name": name,
                "out_degree": out_degrees[uid],
                "max_amount": max_amt
            })

    # Sort: max_amount desc, out_degree desc, user_id asc
    results.sort(key=lambda x: (-x['max_amount'], -x['out_degree'], x['user_id']))

    # Pagination: page 2, size 2 -> slice [2:4]
    return results[2:4]

def test_go_file_exists():
    assert os.path.exists('/home/user/process.go'), "/home/user/process.go does not exist. Did you write the Go program?"

def test_output_json_exists():
    assert os.path.exists('/home/user/output.json'), "/home/user/output.json does not exist. Did you compile and run the program?"

def test_output_json_content():
    with open('/home/user/output.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/output.json is not valid JSON")

    expected = get_expected_output()

    assert isinstance(data, list), "Output JSON must be an array (list)"
    assert len(data) == len(expected), f"Expected {len(expected)} items in the paginated output, but got {len(data)}"

    for i, (act, exp) in enumerate(zip(data, expected)):
        assert act.get("user_id") == exp["user_id"], f"Item {i}: expected user_id {exp['user_id']}, got {act.get('user_id')}"
        assert act.get("name") == exp["name"], f"Item {i}: expected name '{exp['name']}', got '{act.get('name')}'"
        assert act.get("out_degree") == exp["out_degree"], f"Item {i}: expected out_degree {exp['out_degree']}, got {act.get('out_degree')}"

        act_amount = act.get("max_amount")
        assert act_amount is not None, f"Item {i}: missing 'max_amount'"
        assert float(act_amount) == exp["max_amount"], f"Item {i}: expected max_amount {exp['max_amount']}, got {act_amount}"