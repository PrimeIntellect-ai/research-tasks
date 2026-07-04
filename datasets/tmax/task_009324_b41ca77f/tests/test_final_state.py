# test_final_state.py

import os
import csv
import sqlite3
import pytest

LOG_PATH = "/home/user/access.log"
CPP_PATH = "/home/user/log_analyzer.cpp"
EXE_PATH = "/home/user/log_analyzer"
CSV_PATH = "/home/user/endpoint_stats.csv"
DB_PATH = "/home/user/log_stats.db"

def compute_expected_stats(log_path):
    stats = {}
    valid_methods = {"GET", "POST", "PUT", "DELETE"}

    with open(log_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 7:
                continue

            _, _, method, endpoint, _, status_code_str, response_time_str = parts

            if method not in valid_methods:
                continue

            try:
                status_code = int(status_code_str)
                if status_code <= 0:
                    continue
            except ValueError:
                continue

            try:
                response_time = int(response_time_str)
                if response_time < 0:
                    continue
            except ValueError:
                continue

            if endpoint not in stats:
                stats[endpoint] = {"total": 0, "success": 0, "time_sum": 0}

            stats[endpoint]["total"] += 1
            if status_code == 200:
                stats[endpoint]["success"] += 1
            stats[endpoint]["time_sum"] += response_time

    expected_csv = []
    for ep in sorted(stats.keys()):
        total = stats[ep]["total"]
        success = stats[ep]["success"]
        avg_time = stats[ep]["time_sum"] // total
        expected_csv.append({
            "endpoint": ep,
            "total_requests": str(total),
            "success_requests": str(success),
            "avg_response_time": str(avg_time)
        })

    return expected_csv

def test_files_exist():
    assert os.path.isfile(CPP_PATH), f"C++ source file {CPP_PATH} does not exist."
    assert os.path.isfile(EXE_PATH), f"Executable {EXE_PATH} does not exist."
    assert os.path.isfile(CSV_PATH), f"CSV file {CSV_PATH} does not exist."
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

def test_csv_content():
    expected_rows = compute_expected_stats(LOG_PATH)

    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["endpoint", "total_requests", "success_requests", "avg_response_time"], \
            "CSV header does not match expected exact header."

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), "Number of rows in CSV does not match expected."

    for actual, expected in zip(actual_rows, expected_rows):
        assert actual["endpoint"] == expected["endpoint"], f"Expected endpoint {expected['endpoint']}, got {actual['endpoint']}"
        assert actual["total_requests"] == expected["total_requests"], f"Expected total_requests {expected['total_requests']} for {expected['endpoint']}"
        assert actual["success_requests"] == expected["success_requests"], f"Expected success_requests {expected['success_requests']} for {expected['endpoint']}"
        assert actual["avg_response_time"] == expected["avg_response_time"], f"Expected avg_response_time {expected['avg_response_time']} for {expected['endpoint']}"

def test_sqlite_db_content():
    expected_rows = compute_expected_stats(LOG_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='endpoint_stats';")
    assert cursor.fetchone() is not None, "Table 'endpoint_stats' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(endpoint_stats);")
    columns = cursor.fetchall()

    col_dict = {col[1]: {"type": col[2].upper(), "pk": col[5]} for col in columns}

    assert "endpoint" in col_dict, "Column 'endpoint' missing in table schema."
    assert "TEXT" in col_dict["endpoint"]["type"], "Column 'endpoint' should be TEXT."
    assert col_dict["endpoint"]["pk"] == 1, "Column 'endpoint' should be the PRIMARY KEY."

    for num_col in ["total_requests", "success_requests", "avg_response_time"]:
        assert num_col in col_dict, f"Column '{num_col}' missing in table schema."
        assert "INT" in col_dict[num_col]["type"], f"Column '{num_col}' should be INTEGER."

    # Check data
    cursor.execute("SELECT endpoint, total_requests, success_requests, avg_response_time FROM endpoint_stats ORDER BY endpoint;")
    db_rows = cursor.fetchall()

    assert len(db_rows) == len(expected_rows), "Number of rows in database does not match expected."

    for db_row, expected in zip(db_rows, expected_rows):
        assert db_row[0] == expected["endpoint"], "Endpoint mismatch in DB."
        assert str(db_row[1]) == expected["total_requests"], f"total_requests mismatch for {expected['endpoint']} in DB."
        assert str(db_row[2]) == expected["success_requests"], f"success_requests mismatch for {expected['endpoint']} in DB."
        assert str(db_row[3]) == expected["avg_response_time"], f"avg_response_time mismatch for {expected['endpoint']} in DB."

    conn.close()