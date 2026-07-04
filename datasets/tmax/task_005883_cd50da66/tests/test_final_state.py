# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest

def test_analyze_script_exists():
    assert os.path.isfile("/home/user/analyze.py"), "The script /home/user/analyze.py does not exist."

def test_script_execution_and_output():
    script_path = "/home/user/analyze.py"
    output_path = "/home/user/output.json"

    # Run the script to ensure it generates the correct output for the specified parameters
    result = subprocess.run(
        ["python3", script_path, "/api/checkout", "5", "2"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with error:\n{result.stderr}"

    assert os.path.isfile(output_path), f"Output file missing at {output_path} after running the script."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    assert isinstance(data, list), "Output JSON should be a list of objects."

    # Recompute expected truth from DB
    db_path = "/home/user/metrics.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Compute using python to be principled and independent of the student's SQL
    c.execute(
        "SELECT id, endpoint, response_time_ms, timestamp FROM api_requests WHERE endpoint = ? ORDER BY timestamp ASC",
        ("/api/checkout",)
    )
    rows = c.fetchall()
    conn.close()

    expected = []
    prev_time = None
    for row in rows:
        row_id, endpoint, resp_time, ts = row
        diff = resp_time - prev_time if prev_time is not None else None
        expected.append({
            "id": row_id,
            "endpoint": endpoint,
            "response_time_ms": resp_time,
            "timestamp": ts,
            "prev_response_time_ms": prev_time,
            "time_diff": diff
        })
        prev_time = resp_time

    # Sort DESC by timestamp and apply limit 5, offset 2
    expected.sort(key=lambda x: x["timestamp"], reverse=True)
    expected_paginated = expected[2:7]

    assert len(data) == len(expected_paginated), f"Expected {len(expected_paginated)} results, got {len(data)}."

    for i, (actual_row, expected_row) in enumerate(zip(data, expected_paginated)):
        assert actual_row.get("id") == expected_row["id"], f"Row {i} id mismatch. Expected {expected_row['id']}, got {actual_row.get('id')}."
        assert actual_row.get("endpoint") == expected_row["endpoint"], f"Row {i} endpoint mismatch."
        assert actual_row.get("response_time_ms") == expected_row["response_time_ms"], f"Row {i} response_time_ms mismatch."
        assert actual_row.get("timestamp") == expected_row["timestamp"], f"Row {i} timestamp mismatch."
        assert actual_row.get("prev_response_time_ms") == expected_row["prev_response_time_ms"], f"Row {i} prev_response_time_ms mismatch."

        if expected_row["time_diff"] is None:
            assert actual_row.get("time_diff") is None, f"Row {i} time_diff mismatch. Expected None."
        else:
            assert actual_row.get("time_diff") is not None, f"Row {i} time_diff mismatch. Expected {expected_row['time_diff']}, got None."
            assert abs(actual_row["time_diff"] - expected_row["time_diff"]) < 1e-5, f"Row {i} time_diff mismatch. Expected {expected_row['time_diff']}, got {actual_row['time_diff']}."