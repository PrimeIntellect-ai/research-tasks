# test_final_state.py

import os
import sqlite3
import json
import statistics
import pytest

def test_recovered_database_exists_and_valid():
    db_path = "/home/user/telemetry_recovered.db"
    assert os.path.exists(db_path), f"Recovered database not found at {db_path}"

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, payload FROM readings")
        rows = cur.fetchall()
        conn.close()
    except sqlite3.DatabaseError as e:
        pytest.fail(f"Recovered database is malformed or invalid: {e}")

    assert len(rows) > 0, "Recovered database is empty. Expected it to contain the recovered records."

def test_anomalies_file_correct():
    db_path = "/home/user/telemetry_recovered.db"
    assert os.path.exists(db_path), "Cannot verify anomalies because recovered database is missing."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, payload FROM readings")
        rows = cur.fetchall()
    except sqlite3.DatabaseError:
        pytest.fail("Recovered database is malformed, cannot verify anomalies.")
    finally:
        conn.close()

    temps = []
    parsed_data = []

    for r_id, payload in rows:
        try:
            payload_str = payload.decode('utf-8')
        except UnicodeDecodeError:
            payload_str = payload.decode('latin-1')

        data = json.loads(payload_str)
        temp = data['temp']
        temps.append(temp)
        parsed_data.append((r_id, temp))

    if len(temps) < 2:
        pytest.fail("Not enough records in the recovered database to calculate standard deviation.")

    mean_temp = statistics.mean(temps)
    stdev_temp = statistics.stdev(temps)

    expected_anomalies = []
    for r_id, temp in parsed_data:
        z_score = (temp - mean_temp) / stdev_temp
        if z_score > 3:
            expected_anomalies.append(str(r_id))

    expected_anomalies.sort(key=int)

    anomalies_path = "/home/user/anomalies.txt"
    assert os.path.exists(anomalies_path), f"Anomalies file not found at {anomalies_path}"

    with open(anomalies_path, "r") as f:
        actual_anomalies = [line.strip() for line in f if line.strip()]

    assert actual_anomalies == expected_anomalies, (
        f"Anomalies file contents do not match expected. "
        f"Expected: {expected_anomalies}, Got: {actual_anomalies}"
    )