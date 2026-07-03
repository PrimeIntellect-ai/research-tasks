# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest
import statistics

def test_recovered_database():
    db_path = "/home/user/recovered_data.db"
    assert os.path.isfile(db_path), f"Recovered database missing at {db_path}"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sensors")
        count = cursor.fetchone()[0]
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Could not read from recovered database: {e}")

    assert count == 3, f"Expected 3 rows in recovered database, found {count}"

def test_processed_output():
    out_path = "/home/user/processed_output.json"
    assert os.path.isfile(out_path), f"Processed output missing at {out_path}"

    with open(out_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Processed output is not valid JSON")

    assert isinstance(data, list), "Processed output should be a JSON list"
    assert len(data) == 3, f"Expected 3 records in processed output, found {len(data)}"

    for record in data:
        assert "id" in record, "Record missing 'id'"
        assert "variance" in record, "Record missing 'variance'"
        assert isinstance(record["variance"], float) or isinstance(record["variance"], int), "Variance should be a number"
        assert record["variance"] > 0, "Variance should be strictly positive (not zero or negative due to catastrophic cancellation)"

def test_service_memory_leak_fixed():
    service_path = "/home/user/service.py"
    assert os.path.isfile(service_path), f"Service file missing at {service_path}"

    with open(service_path, "r") as f:
        content = f.read()

    has_discard = "active_tasks.discard" in content
    has_remove = "active_tasks.remove" in content
    has_add = "active_tasks.add" in content

    fixed = has_discard or has_remove or not has_add
    assert fixed, "Memory leak in service.py is not fixed (tasks are added to active_tasks but never removed)"

def test_regression_test():
    test_path = "/home/user/test_regression.py"
    assert os.path.isfile(test_path), f"Regression test file missing at {test_path}"

    # Run the user's unittest suite
    result = subprocess.run(
        ["python", "-m", "unittest", test_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Regression tests failed:\n{result.stdout}\n{result.stderr}"

def test_fix_summary():
    log_path = "/home/user/fix_summary.log"
    assert os.path.isfile(log_path), f"Summary log missing at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, f"Expected at least 3 lines in summary log, found {len(lines)}"

    assert lines[0] == "3", f"Line 1 (rows recovered) should be '3', got '{lines[0]}'"

    try:
        variance = float(lines[1])
    except ValueError:
        pytest.fail(f"Line 2 (variance) could not be parsed as float: '{lines[1]}'")

    # Python statistics module variance for the sample
    expected_var = statistics.variance([100000000.0, 100000000.00001, 100000000.00002])
    assert 0 < variance < 1e-9, f"Line 2 (variance) is not in the expected range. Got {variance}, expected close to {expected_var}"

    assert lines[2] == "3", f"Line 3 (last record id) should be '3', got '{lines[2]}'"