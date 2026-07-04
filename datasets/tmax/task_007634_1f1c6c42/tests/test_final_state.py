# test_final_state.py

import os
import sqlite3
import pytest
from datetime import datetime

BASE_DIR = "/home/user/ticket_8832"

def test_timeline_log_sorted_and_complete():
    timeline_path = os.path.join(BASE_DIR, "timeline.log")
    assert os.path.isfile(timeline_path), f"File missing: {timeline_path}"

    # Read original logs to get all lines
    logs_dir = os.path.join(BASE_DIR, "logs")
    original_lines = []
    for log_file in ["node_A.log", "node_B.log", "node_C.log"]:
        log_path = os.path.join(logs_dir, log_file)
        if os.path.isfile(log_path):
            with open(log_path, "r") as f:
                original_lines.extend([line.strip() for line in f if line.strip()])

    with open(timeline_path, "r") as f:
        timeline_lines = [line.strip() for line in f if line.strip()]

    # Check completeness
    assert sorted(original_lines) == sorted(timeline_lines), "timeline.log does not contain the exact same lines as the original logs"

    # Check sorting
    timestamps = []
    for line in timeline_lines:
        # Extract timestamp, assuming ISO format at the beginning of the line
        ts_str = line.split(" ")[0]
        try:
            ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
            timestamps.append(ts)
        except ValueError:
            pytest.fail(f"Could not parse timestamp from line: {line}")

    assert timestamps == sorted(timestamps), "timeline.log is not sorted chronologically"


def test_source_code_fixed():
    cpp_path = os.path.join(BASE_DIR, "src", "optimizer.cpp")
    assert os.path.isfile(cpp_path), f"Source file missing: {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "short iterations" not in content, "optimizer.cpp still contains 'short iterations' (integer overflow bug)"
    assert "float x" not in content, "optimizer.cpp still contains 'float x' (precision loss bug)"
    assert "float prev_x" not in content, "optimizer.cpp still contains 'float prev_x' (precision loss bug)"


def test_database_has_successful_run():
    db_path = os.path.join(BASE_DIR, "db", "results.db")
    assert os.path.isfile(db_path), f"Database file missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check for successful run with input 2500.0
    cursor.execute("SELECT result_value, status FROM convergence_runs WHERE input_value = 2500.0 ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()

    assert row is not None, "No run found for input_value = 2500.0 in the database"
    result_value, status = row

    assert status == "SUCCESS", f"Expected status 'SUCCESS' for input 2500.0, got '{status}'"
    assert abs(result_value - 5.0) < 1e-4, f"Expected result_value close to 5.0, got {result_value}"

    conn.close()


def test_final_answer_file():
    answer_path = os.path.join(BASE_DIR, "final_answer.txt")
    assert os.path.isfile(answer_path), f"Final answer file missing: {answer_path}"

    with open(answer_path, "r") as f:
        content = f.read().strip()

    assert content == "5.0000", f"Expected final_answer.txt to contain exactly '5.0000', got '{content}'"