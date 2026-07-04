# test_final_state.py
import os
import sqlite3
import json
import itertools
import pytest

def test_optimize_sql_exists_and_valid():
    """Verify that optimize.sql exists and contains a valid index creation statement."""
    sql_path = '/home/user/optimize.sql'
    assert os.path.exists(sql_path), f"{sql_path} does not exist."

    with open(sql_path, 'r') as f:
        content = f.read().lower()

    assert "create " in content and " index " in content, \
        f"{sql_path} must contain a CREATE INDEX statement."

    assert "json_extract" in content or "->>" in content or "->" in content, \
        f"{sql_path} must use JSON extraction functions or operators to index the JSON fields."

def test_matching_users_output():
    """Verify that matching_users.txt contains the correct user pairs computed from the DB."""
    db_path = '/home/user/data_lake.db'
    out_path = '/home/user/matching_users.txt'

    assert os.path.exists(db_path), f"{db_path} does not exist."
    assert os.path.exists(out_path), f"{out_path} does not exist."

    # Compute the expected pairs dynamically from the database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT doc FROM documents")

    user_purchases = {}
    for (doc_str,) in cur.fetchall():
        try:
            doc = json.loads(doc_str)
            if doc.get("type") == "purchase":
                uid = doc.get("user_id")
                pid = doc.get("product_id")
                if uid and pid:
                    user_purchases.setdefault(uid, set()).add(pid)
        except json.JSONDecodeError:
            continue

    conn.close()

    expected_pairs = []
    users = sorted(list(user_purchases.keys()))
    for u1, u2 in itertools.combinations(users, 2):
        shared_products = user_purchases[u1].intersection(user_purchases[u2])
        if len(shared_products) == 3:
            expected_pairs.append(f"{u1},{u2}")

    expected_pairs.sort()

    # Read the actual output
    with open(out_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_pairs, \
        f"Output in {out_path} is incorrect. Expected {expected_pairs}, but got {actual_lines}"