# test_final_state.py

import os
import json
import sqlite3
import csv
import glob
from collections import defaultdict

def test_database_exists_and_populated():
    db_path = "/home/user/metrics.db"
    assert os.path.exists(db_path), f"Database not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='server_metrics';")
    table = cursor.fetchone()
    assert table is not None, "Table 'server_metrics' does not exist in the database."

    # Count rows in DB
    cursor.execute("SELECT COUNT(*) FROM server_metrics;")
    db_row_count = cursor.fetchone()[0]

    # Count rows in CSVs
    csv_files = glob.glob("/home/user/data/*.csv")
    csv_row_count = 0
    for f in csv_files:
        with open(f, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip header
            csv_row_count += sum(1 for _ in reader)

    assert db_row_count == csv_row_count, f"Expected {csv_row_count} rows in server_metrics, found {db_row_count}."
    conn.close()

def test_anomalies_json_matches_truth():
    json_path = "/home/user/anomalies.json"
    assert os.path.exists(json_path), f"Anomalies JSON not found at {json_path}"

    # Recompute truth from CSVs
    csv_files = glob.glob("/home/user/data/*.csv")
    daily_cpu = defaultdict(list)

    for f in csv_files:
        with open(f, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date = row["timestamp"].split("T")[0]
                daily_cpu[date].append(float(row["cpu_usage"]))

    daily_avg = {date: sum(cpus)/len(cpus) for date, cpus in daily_cpu.items()}
    sorted_dates = sorted(daily_avg.keys())

    expected_anomalies = []
    for i in range(1, len(sorted_dates)):
        prev_date = sorted_dates[i-1]
        curr_date = sorted_dates[i]
        if daily_avg[curr_date] > 1.5 * daily_avg[prev_date]:
            expected_anomalies.append(curr_date)

    with open(json_path, "r") as jf:
        try:
            data = json.load(jf)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {json_path}")

    assert "anomalies" in data, "JSON missing 'anomalies' key."
    assert data["anomalies"] == expected_anomalies, f"Expected anomalies {expected_anomalies}, got {data['anomalies']}."

def test_pipeline_log_format_and_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Log file not found at {log_path}"

    expected_sequence = [
        "INFO:DAG:Starting task init_db",
        "INFO:DAG:Completed task init_db",
        "INFO:DAG:Starting task load_data",
        "INFO:DAG:Completed task load_data",
        "INFO:DAG:Starting task detect_anomalies",
        "INFO:DAG:Completed task detect_anomalies",
        "INFO:DAG:Starting task export_results",
        "INFO:DAG:Completed task export_results"
    ]

    with open(log_path, "r") as lf:
        log_lines = [line.strip() for line in lf if line.strip()]

    # Filter out lines that might not be from our logger, though there shouldn't be any
    dag_lines = [line for line in log_lines if line.startswith("INFO:DAG:")]

    assert dag_lines == expected_sequence, "Log lines do not match the expected DAG execution sequence."