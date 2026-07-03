# test_final_state.py
import os
import sqlite3
import shutil
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def get_expected_report():
    db_path = "/app/trading.db"
    test_db_path = "/tmp/test_trading.db"
    if not os.path.exists(db_path):
        pytest.fail(f"Database {db_path} is missing.")

    shutil.copy(db_path, test_db_path)
    conn = sqlite3.connect(test_db_path)
    try:
        conn.execute("DROP INDEX IF EXISTS idx_trades_user")
    except sqlite3.Error:
        pass

    cur = conn.cursor()
    cur.execute("SELECT id, amount FROM trades WHERE user_id = 83 ORDER BY trade_date")
    trades = cur.fetchall()

    expected_report = []
    for i in range(len(trades)):
        start = max(0, i - 3)
        prev_trades = trades[start:i]
        if not prev_trades:
            continue
        rolling_avg = sum(t[1] for t in prev_trades) / len(prev_trades)
        if trades[i][1] > rolling_avg:
            expected_report.append({
                "trade_id": trades[i][0],
                "amount": float(trades[i][1]),
                "rolling_avg": float(rolling_avg)
            })

    conn.close()
    return expected_report

def test_target_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/target", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/target: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /target is not valid JSON: {response.text}")

    assert "target_user" in data, "Missing 'target_user' in /target response"
    assert data["target_user"] == 83, f"Expected target_user 83, got {data['target_user']}"

def test_report_endpoint():
    expected_report = get_expected_report()

    try:
        response = requests.get(f"{BASE_URL}/report", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/report: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /report is not valid JSON: {response.text}")

    assert isinstance(data, list), "Expected /report to return a JSON array"

    # Compare by trade_id to be robust against floating point differences
    expected_trade_ids = [t["trade_id"] for t in expected_report]
    actual_trade_ids = [t.get("trade_id") for t in data]

    assert sorted(actual_trade_ids) == sorted(expected_trade_ids), \
        f"Expected trade IDs {expected_trade_ids}, got {actual_trade_ids}"

    # Check structure
    if data:
        assert "amount" in data[0], "Missing 'amount' in report item"
        assert "rolling_avg" in data[0], "Missing 'rolling_avg' in report item"