# test_final_state.py

import os
import sqlite3
import json
import csv
import pytest

def test_task1_fixed_sql_report():
    csv_path = "/home/user/fixed_sql_report.csv"
    db_path = "/home/user/backups.db"

    assert os.path.exists(csv_path), f"File {csv_path} is missing."

    # Derive expected result from DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.hostname, SUM(b.size_mb) as total_size_mb
        FROM servers s
        JOIN backup_jobs b ON s.id = b.server_id
        WHERE b.status = 'SUCCESS'
        GROUP BY s.hostname
        ORDER BY total_size_mb DESC;
    """)
    expected_rows = cursor.fetchall()
    conn.close()

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{csv_path} is empty."
    assert rows[0] == ['hostname', 'total_size_mb'], f"Headers in {csv_path} are incorrect. Expected ['hostname', 'total_size_mb'], got {rows[0]}"

    actual_data = [(row[0], int(row[1])) for row in rows[1:] if len(row) == 2]

    assert actual_data == expected_rows, f"Data in {csv_path} does not match expected derived data. Expected {expected_rows}, got {actual_data}"

def test_task2_get_chain_script_and_result():
    script_path = "/home/user/get_chain.sh"
    result_path = "/home/user/chain_result.txt"
    db_path = "/home/user/backups.db"

    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    assert os.path.exists(result_path), f"Result file {result_path} is missing."

    # Derive expected chain for 'incr_999'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    current_id = 'incr_999'
    chain = [current_id]

    while True:
        cursor.execute("SELECT parent_id FROM backup_lineage WHERE child_id = ?", (current_id,))
        row = cursor.fetchone()
        if row and row[0]:
            current_id = row[0]
            chain.append(current_id)
        else:
            break

    conn.close()
    expected_chain_str = "->".join(chain)

    with open(result_path, 'r') as f:
        actual_chain_str = f.read().strip()

    assert actual_chain_str == expected_chain_str, f"Chain result in {result_path} is incorrect. Expected '{expected_chain_str}', got '{actual_chain_str}'"

def test_task3_nosql_summary_script_and_report():
    script_path = "/home/user/nosql_summary.sh"
    csv_path = "/home/user/nosql_report.csv"
    json_path = "/home/user/nosql_backups.json"

    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    assert os.path.exists(csv_path), f"File {csv_path} is missing."

    # Derive expected result from JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Filter SUCCESS and find latest timestamp per cluster
    clusters = {}
    for job in data:
        if job.get('status') == 'SUCCESS':
            cid = job['cluster_id']
            ts = job['timestamp']
            if cid not in clusters or ts > clusters[cid]['timestamp']:
                clusters[cid] = job

    expected_rows = sorted([(cid, clusters[cid]['size_gb']) for cid in clusters])

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{csv_path} is empty."
    assert rows[0] == ['cluster_id', 'latest_size_gb'], f"Headers in {csv_path} are incorrect. Expected ['cluster_id', 'latest_size_gb'], got {rows[0]}"

    actual_data = [(row[0], int(row[1])) for row in rows[1:] if len(row) == 2]

    assert actual_data == expected_rows, f"Data in {csv_path} does not match expected derived data. Expected {expected_rows}, got {actual_data}"