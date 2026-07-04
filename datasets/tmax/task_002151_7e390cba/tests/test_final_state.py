# test_final_state.py

import os
import sqlite3
import requests
import csv
from datetime import datetime

def test_database_exists():
    path = "/home/user/analytics.db"
    assert os.path.isfile(path), f"Database not found at {path}"

def test_api_invalid_token():
    url = "http://127.0.0.1:9090/insights"
    headers = {"X-API-Token": "invalid-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to API: {e}"

    assert response.status_code in (401, 403), f"Expected 401 or 403 for invalid token, got {response.status_code}"

def test_api_valid_token_and_schema():
    url = "http://127.0.0.1:9090/insights"
    headers = {"X-API-Token": "sierra-tango-99"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to API: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code} with body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, "API did not return valid JSON"

    assert isinstance(data, list), "Expected JSON response to be a list"

    for item in data:
        assert isinstance(item, dict), "Each item in the list must be a JSON object"
        assert "customer_id" in item, "Missing 'customer_id' in response object"
        assert "rolling_amount" in item, "Missing 'rolling_amount' in response object"
        assert "latest_call_duration" in item, "Missing 'latest_call_duration' in response object"

        assert isinstance(item["customer_id"], int), "'customer_id' must be an integer"
        assert isinstance(item["rolling_amount"], (int, float)), "'rolling_amount' must be a float/int"
        assert isinstance(item["latest_call_duration"], int), "'latest_call_duration' must be an integer"

def test_api_correctness():
    # Compute the expected result independently
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("CREATE TABLE transactions (tx_id TEXT, customer_id INTEGER, tx_date TEXT, amount REAL)")
    cur.execute("CREATE TABLE calls (call_id TEXT, customer_id INTEGER, call_date TEXT, duration_seconds INTEGER)")

    with open('/home/user/transactions.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO transactions VALUES (?, ?, ?, ?)", 
                        (row['tx_id'], int(row['customer_id']), row['tx_date'], float(row['amount'])))

    with open('/home/user/calls.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO calls VALUES (?, ?, ?, ?)", 
                        (row['call_id'], int(row['customer_id']), row['call_date'], int(row['duration_seconds'])))

    query = """
    WITH latest_tx AS (
        SELECT customer_id, MAX(tx_date) as max_tx_date
        FROM transactions
        GROUP BY customer_id
    ),
    rolling_sums AS (
        SELECT t.customer_id, SUM(t.amount) as rolling_amount
        FROM transactions t
        JOIN latest_tx lt ON t.customer_id = lt.customer_id
        WHERE t.tx_date >= date(lt.max_tx_date, '-7 days') AND t.tx_date <= lt.max_tx_date
        GROUP BY t.customer_id
    ),
    latest_call AS (
        SELECT customer_id, duration_seconds as latest_call_duration
        FROM (
            SELECT customer_id, duration_seconds,
                   ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY call_date DESC) as rn
            FROM calls
        ) WHERE rn = 1
    )
    SELECT r.customer_id, r.rolling_amount, l.latest_call_duration
    FROM rolling_sums r
    JOIN latest_call l ON r.customer_id = l.customer_id
    """
    cur.execute(query)
    expected_rows = cur.fetchall()

    expected_data = {}
    for row in expected_rows:
        expected_data[row['customer_id']] = {
            'rolling_amount': float(row['rolling_amount']),
            'latest_call_duration': int(row['latest_call_duration'])
        }

    url = "http://127.0.0.1:9090/insights"
    headers = {"X-API-Token": "sierra-tango-99"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

    actual_data = response.json()
    actual_dict = {item['customer_id']: item for item in actual_data}

    assert len(actual_dict) == len(expected_data), f"Expected {len(expected_data)} customers, got {len(actual_dict)}"

    for cid, exp in expected_data.items():
        assert cid in actual_dict, f"Missing customer {cid} in API response"
        act = actual_dict[cid]
        assert abs(act['rolling_amount'] - exp['rolling_amount']) < 1e-5, f"Incorrect rolling_amount for customer {cid}: expected {exp['rolling_amount']}, got {act['rolling_amount']}"
        assert act['latest_call_duration'] == exp['latest_call_duration'], f"Incorrect latest_call_duration for customer {cid}: expected {exp['latest_call_duration']}, got {act['latest_call_duration']}"