# test_final_state.py

import os
import sqlite3
import pytest

def test_wal_file_integrated():
    # The WAL file should be integrated, meaning it's either removed or empty (0 bytes)
    wal_path = '/home/user/metrics_service/data.db-wal'
    if os.path.exists(wal_path):
        assert os.path.getsize(wal_path) == 0, "The WAL file data.db-wal still contains uncommitted records. It must be fully checkpointed/integrated."

def test_final_metric_file_exists():
    final_path = '/home/user/metrics_service/final_metric.txt'
    assert os.path.isfile(final_path), f"The final metric file {final_path} does not exist."

def test_final_metric_value():
    final_path = '/home/user/metrics_service/final_metric.txt'
    with open(final_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"The content of {final_path} is not a valid number: '{content}'")

    # 15.5 + 24.2 + 10.3 = 50.0
    # Multiplier = 459
    # 50.0 * 459 = 22950.0
    expected_value = 22950.0

    assert val == expected_value, f"The calculated metric {val} is incorrect. Expected {expected_value}."