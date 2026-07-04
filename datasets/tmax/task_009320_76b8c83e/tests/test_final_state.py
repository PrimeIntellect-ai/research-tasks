# test_final_state.py

import os
import sqlite3
import math
import pytest

def test_sla_penalty_result_exists():
    result_path = "/home/user/sla_penalty_result.txt"
    assert os.path.exists(result_path), f"Result file {result_path} is missing."
    assert os.path.isfile(result_path), f"{result_path} is not a file."

def test_sla_penalty_result_value():
    db_path = "/home/user/uptime.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch only valid incidents: end_time >= start_time and severity > 0
    cursor.execute("SELECT start_time, end_time, severity FROM incidents WHERE end_time >= start_time AND severity > 0")
    valid_incidents = cursor.fetchall()

    expected_total = 0
    for start, end, sev in valid_incidents:
        duration = end - start
        if duration > 0:
            # The recursive function adds (severity * 10) for every 60-minute chunk or partial chunk
            chunks = math.ceil(duration / 60.0)
            expected_total += chunks * (sev * 10)

    conn.close()

    result_path = "/home/user/sla_penalty_result.txt"
    with open(result_path, 'r') as f:
        result_content = f.read().strip()

    assert result_content.isdigit(), f"Result file {result_path} does not contain a valid integer. Found: '{result_content}'"
    assert int(result_content) == expected_total, f"Expected SLA penalty score to be {expected_total}, but found {result_content}."