# test_final_state.py

import os
import json
import sqlite3
from itertools import combinations
import pytest

DB_PATH = '/home/user/ecommerce.db'
JSON_PATH = '/home/user/top_user_pairs.json'

def compute_expected_pairs(db_path):
    assert os.path.exists(db_path), f"Database file {db_path} is missing."
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = """
        SELECT pu.user_id, pu.product_id
        FROM purchases pu
        JOIN products pr ON pu.product_id = pr.product_id
        WHERE pr.category = 'Electronics'
          AND pu.purchase_date >= '2023-01-01'
    """
    c.execute(query)
    rows = c.fetchall()
    conn.close()

    user_products = {}
    for user_id, product_id in rows:
        user_products.setdefault(user_id, set()).add(product_id)

    pairs = []
    users = sorted(list(user_products.keys()))
    for u1, u2 in combinations(users, 2):
        shared = len(user_products[u1].intersection(user_products[u2]))
        if shared > 0:
            # Ensure user_a < user_b
            user_a, user_b = min(u1, u2), max(u1, u2)
            pairs.append({"user_a": user_a, "user_b": user_b, "weight": shared})

    # Sort by weight DESC, user_a ASC, user_b ASC
    pairs.sort(key=lambda x: (-x["weight"], x["user_a"], x["user_b"]))

    return pairs[:3]

def test_json_file_exists():
    assert os.path.exists(JSON_PATH), f"The output file {JSON_PATH} was not found."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file."

def test_json_file_content():
    expected_pairs = compute_expected_pairs(DB_PATH)

    with open(JSON_PATH, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {JSON_PATH} does not contain valid JSON.")

    assert isinstance(actual_data, list), f"The JSON root should be a list, but got {type(actual_data).__name__}."
    assert len(actual_data) == len(expected_pairs), f"Expected {len(expected_pairs)} pairs, but found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_pairs)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary."
        assert "user_a" in actual, f"Item at index {i} is missing 'user_a'."
        assert "user_b" in actual, f"Item at index {i} is missing 'user_b'."
        assert "weight" in actual, f"Item at index {i} is missing 'weight'."

        assert actual["user_a"] == expected["user_a"], f"Mismatch at index {i} for 'user_a'. Expected {expected['user_a']}, got {actual['user_a']}."
        assert actual["user_b"] == expected["user_b"], f"Mismatch at index {i} for 'user_b'. Expected {expected['user_b']}, got {actual['user_b']}."
        assert actual["weight"] == expected["weight"], f"Mismatch at index {i} for 'weight'. Expected {expected['weight']}, got {actual['weight']}."
        assert actual["user_a"] < actual["user_b"], f"At index {i}, user_a ({actual['user_a']}) is not strictly less than user_b ({actual['user_b']})."