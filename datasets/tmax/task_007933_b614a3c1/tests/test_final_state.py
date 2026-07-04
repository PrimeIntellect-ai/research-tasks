# test_final_state.py

import os
import re
import sqlite3
import pytest

def test_database_recovered():
    db_path = "/home/user/sensor_data.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM sensors")
        count = cursor.fetchone()[0]
        assert count == 50000, f"Expected exactly 50000 rows in 'sensors' table, but found {count}."

        cursor.execute("SELECT SUM(value) FROM sensors")
        total_sum = cursor.fetchone()[0]
        expected_sum = 500008.60
        assert total_sum is not None, "The sum of values is NULL."
        assert abs(total_sum - expected_sum) < 0.01, f"Expected total sum of approximately {expected_sum}, but got {total_sum}."

    except sqlite3.Error as e:
        pytest.fail(f"SQLite error when querying the database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_bottleneck_txt():
    path = "/home/user/bottleneck.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    # Expecting format like openat:/usr/share/zoneinfo/America/New_York
    # Some systems might report 'open' instead of 'openat'
    pattern = r"^(openat?):.*/America/New_York$"
    assert re.match(pattern, content), (
        f"Contents of {path} ('{content}') do not match the expected format "
        "'<syscall>:<filepath>' for the timezone file bottleneck."
    )

def test_mre_c():
    path = "/home/user/mre.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "setenv" in content, f"{path} is missing the 'setenv' call."
    assert "tzset" in content, f"{path} is missing the 'tzset' call."
    assert "sqlite3" not in content, f"{path} should not contain any SQLite code."

    # Check for a loop (for or while)
    assert re.search(r"(for|while)\s*\(", content), f"{path} does not appear to contain a loop."
    # Check for 10000 iterations requirement
    assert "10000" in content, f"{path} should loop for 10,000 iterations."

def test_analyzer_c_fixed():
    path = "/home/user/analyzer.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # The fix should involve caching or checking the previous timezone before calling setenv/tzset
    # This usually means a string comparison function like strcmp or maintaining a previous timezone state.
    assert "strcmp" in content or "strncmp" in content or "!= NULL" in content or "strcpy" in content, (
        f"{path} does not appear to conditionally check the timezone before updating it."
    )

def test_output_txt():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert "500008.6" in content, f"File {path} does not contain the correct expected sum. Content was: '{content}'"