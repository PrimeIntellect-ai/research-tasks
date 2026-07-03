# test_final_state.py

import os
import json
import sqlite3
import csv

def get_expected_vip_revenue():
    events_dir = "/home/user/etl_data/events"
    db_path = "/home/user/etl_data/primary.db"

    # 1. Find VIP customers from JSON files
    vip_user_ids = set()
    if os.path.isdir(events_dir):
        for filename in os.listdir(events_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(events_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        history = data.get("data", {}).get("history", [])
                        for event in history:
                            if event.get("action") == "GRANT_VIP" and "user_ref" in event:
                                vip_user_ids.add(event["user_ref"])
                except Exception:
                    pass

    # 2. Query SQLite for completed revenue
    results = []
    if os.path.isfile(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for user_id in vip_user_ids:
            cursor.execute("SELECT name FROM customers WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                continue
            name = row[0]

            cursor.execute("SELECT SUM(amount) FROM orders WHERE customer_id = ? AND status = 'completed'", (user_id,))
            amount_row = cursor.fetchone()
            total_revenue = amount_row[0] if amount_row and amount_row[0] is not None else 0

            if total_revenue > 0:
                results.append((name, float(total_revenue)))

        conn.close()

    # 3. Sort descending by revenue, then alphabetically by name
    results.sort(key=lambda x: (-x[1], x[0]))
    return results

def test_vip_revenue_csv_exists():
    csv_path = "/home/user/etl_data/vip_revenue.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} was not found."

def test_vip_revenue_csv_content():
    csv_path = "/home/user/etl_data/vip_revenue.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} was not found."

    expected_results = get_expected_vip_revenue()

    actual_results = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Expected 2 columns in CSV, but found {len(row)} in row: {row}"
            name, revenue_str = row
            try:
                revenue = float(revenue_str)
            except ValueError:
                assert False, f"Revenue '{revenue_str}' for customer '{name}' is not a valid number."
            actual_results.append((name.strip(), revenue))

    assert len(actual_results) == len(expected_results), (
        f"Expected {len(expected_results)} rows in CSV, but got {len(actual_results)}. "
        f"Actual names: {[r[0] for r in actual_results]}"
    )

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        actual_name, actual_rev = actual
        expected_name, expected_rev = expected

        assert actual_name == expected_name, (
            f"Row {i+1} mismatch: Expected customer '{expected_name}', but got '{actual_name}'. "
            f"Check sorting or filtering requirements."
        )
        assert abs(actual_rev - expected_rev) < 1e-5, (
            f"Row {i+1} mismatch for customer '{actual_name}': Expected revenue {expected_rev}, but got {actual_rev}."
        )