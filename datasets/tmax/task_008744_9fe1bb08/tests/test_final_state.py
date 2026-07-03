# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/transactions.db'
OUTPUT_PATH = '/home/user/flagged_anomalies.json'

def get_expected_anomalies():
    """Compute expected anomalies directly from the database to align with the truth."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, user_id, timestamp, amount FROM transactions ORDER BY user_id, timestamp ASC")
    rows = cursor.fetchall()
    conn.close()

    users = {}
    for row in rows:
        users.setdefault(row['user_id'], []).append(row)

    anomalies = []
    for user_id, transactions in users.items():
        for i in range(4, len(transactions)):
            window = transactions[i-4:i+1]
            avg = sum(t['amount'] for t in window) / 5.0
            current_tx = transactions[i]
            if current_tx['amount'] > 2.0 * avg:
                anomalies.append({
                    "transaction_id": current_tx['id'],
                    "user_id": current_tx['user_id'],
                    "timestamp": current_tx['timestamp'],
                    "amount": float(current_tx['amount']),
                    "moving_average": round(avg, 2)
                })

    return anomalies

def test_json_file_exists():
    """Verify that the output JSON file exists."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."

def test_json_format_and_schema():
    """Verify that the output file is valid JSON and matches the required schema."""
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON root must be an array."

    for i, item in enumerate(data):
        assert isinstance(item, dict), f"Item at index {i} is not a JSON object."
        assert "transaction_id" in item, f"Item at index {i} missing 'transaction_id'."
        assert isinstance(item["transaction_id"], int), f"Item at index {i} 'transaction_id' is not an integer."

        assert "user_id" in item, f"Item at index {i} missing 'user_id'."
        assert isinstance(item["user_id"], str), f"Item at index {i} 'user_id' is not a string."

        assert "timestamp" in item, f"Item at index {i} missing 'timestamp'."
        assert isinstance(item["timestamp"], int), f"Item at index {i} 'timestamp' is not an integer."

        assert "amount" in item, f"Item at index {i} missing 'amount'."
        assert isinstance(item["amount"], (int, float)), f"Item at index {i} 'amount' is not a float."

        assert "moving_average" in item, f"Item at index {i} missing 'moving_average'."
        assert isinstance(item["moving_average"], (int, float)), f"Item at index {i} 'moving_average' is not a float."

def test_anomalies_correctness():
    """Verify that the anomalies in the JSON file correctly match the expected ones."""
    with open(OUTPUT_PATH, 'r') as f:
        data = json.load(f)

    expected = get_expected_anomalies()

    assert len(data) == len(expected), f"Expected {len(expected)} anomalies, but found {len(data)}."

    # Sort both lists by transaction_id to compare them easily
    data_sorted = sorted(data, key=lambda x: x["transaction_id"])
    expected_sorted = sorted(expected, key=lambda x: x["transaction_id"])

    for act, exp in zip(data_sorted, expected_sorted):
        assert act["transaction_id"] == exp["transaction_id"], f"Transaction ID mismatch: expected {exp['transaction_id']}, got {act['transaction_id']}."
        assert act["user_id"] == exp["user_id"], f"User ID mismatch for tx {exp['transaction_id']}."
        assert act["timestamp"] == exp["timestamp"], f"Timestamp mismatch for tx {exp['transaction_id']}."
        assert act["amount"] == exp["amount"], f"Amount mismatch for tx {exp['transaction_id']}."
        assert round(act["moving_average"], 2) == exp["moving_average"], f"Moving average mismatch for tx {exp['transaction_id']}: expected {exp['moving_average']}, got {act['moving_average']}."