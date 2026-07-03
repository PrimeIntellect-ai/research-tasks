# test_final_state.py
import os
import json
import time
import sqlite3
import subprocess
import pytest

def get_expected_flagged_users():
    db_path = '/app/data/audit_logs.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all users, their total events, and distinct IPs
    cursor.execute("""
        SELECT u_id, COUNT(event_id), COUNT(DISTINCT ip_address)
        FROM access_events
        GROUP BY u_id
    """)
    user_stats = cursor.fetchall()

    flagged_users = []
    for u_id, total_events, distinct_ips in user_stats:
        if distinct_ips > 0:
            score = 1.0 - (total_events / (distinct_ips * 10.0))
            if score < 0:
                score = 0.0
            if score > 0.80:
                flagged_users.append(u_id)

    # Calculate total tx amount for flagged users
    expected_results = {}
    if flagged_users:
        placeholders = ','.join(['?'] * len(flagged_users))
        cursor.execute(f"""
            SELECT u_id, SUM(amount)
            FROM tx_data
            WHERE u_id IN ({placeholders})
            GROUP BY u_id
        """, flagged_users)

        for u_id, total_amount in cursor.fetchall():
            expected_results[u_id] = round(total_amount, 2)

    conn.close()
    return expected_results

def test_audit_aggregator_execution_and_output():
    script_path = '/home/user/audit_aggregator.py'
    output_path = '/home/user/flagged_users.json'

    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    # Remove output file if it exists to ensure we measure fresh generation
    if os.path.exists(output_path):
        os.remove(output_path)

    start_time = time.time()
    proc = subprocess.run(["python3", script_path], capture_output=True, text=True)
    runtime = time.time() - start_time

    assert proc.returncode == 0, f"Script failed to execute. stderr: {proc.stderr}"
    assert runtime < 3.0, f"Execution time={runtime:.2f}s exceeded threshold of 3.0s"

    assert os.path.isfile(output_path), f"Output file missing at {output_path}"

    with open(output_path, 'r') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON")

    expected_results = get_expected_flagged_users()

    # Check exact match
    assert set(actual_results.keys()) == set(expected_results.keys()), \
        f"Keys mismatch. Expected: {list(expected_results.keys())}, Got: {list(actual_results.keys())}"

    for k, expected_val in expected_results.items():
        actual_val = actual_results[k]
        assert abs(actual_val - expected_val) < 1e-5, \
            f"Value mismatch for user {k}. Expected: {expected_val}, Got: {actual_val}"