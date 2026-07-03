# test_final_state.py

import os
import json
import pytest

def compute_expected_csv():
    users_path = "/home/user/users.jsonl"
    orders_path = "/home/user/orders.jsonl"

    if not os.path.exists(users_path) or not os.path.exists(orders_path):
        return ""

    users = {}
    with open(users_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                u = json.loads(line)
                users[u['user_id']] = u.get('region', '')

    totals = {}
    with open(orders_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                o = json.loads(line)
                if o.get('status') == 'completed' and o.get('total', 0) > 100:
                    uid = o['user_id']
                    totals[uid] = totals.get(uid, 0) + o['total']

    results = []
    for uid, total in totals.items():
        results.append((uid, users.get(uid, ""), total))

    # Sort descending by total_spent, then ascending by user_id
    results.sort(key=lambda x: (-x[2], x[0]))

    # Paginate: skip 1, limit 3
    paginated = results[1:4]

    lines = ["user_id,region,total_spent"]
    for r in paginated:
        lines.append(f"{r[0]},{r[1]},{r[2]}")

    return "\n".join(lines)

def test_aggregate_c_exists():
    path = "/home/user/aggregate.c"
    assert os.path.exists(path), f"The C source file {path} is missing."
    assert os.path.isfile(path), f"The path {path} must be a regular file."

def test_results_csv_exists():
    path = "/home/user/results.csv"
    assert os.path.exists(path), f"The output file {path} is missing. Did you compile and run your C program?"
    assert os.path.isfile(path), f"The path {path} must be a regular file."

def test_results_csv_content():
    path = "/home/user/results.csv"
    assert os.path.exists(path), f"Cannot verify content because {path} is missing."

    with open(path, 'r') as f:
        actual_content = f.read().strip()

    expected_content = compute_expected_csv().strip()

    assert expected_content != "", "Could not compute expected CSV because input files are missing or invalid."

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {path} does not match the expected aggregation pipeline output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )