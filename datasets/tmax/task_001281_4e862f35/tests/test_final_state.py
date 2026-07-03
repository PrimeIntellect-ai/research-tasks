# test_final_state.py

import os
import re
import pytest

def test_aggregate_script_exists_and_uses_flock():
    script_path = "/home/user/aggregate.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for fcntl.flock and LOCK_EX
    assert "fcntl" in content, "The script does not import or use fcntl."
    assert "flock" in content, "The script does not use fcntl.flock."
    assert "LOCK_EX" in content, "The script does not use LOCK_EX for exclusive locking."

def test_summary_log_exists_and_correct():
    log_path = "/home/user/summary.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the script?"

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    expected_line = "experiment_B.zip/sensor_readings.csv SUM:400"

    # The file should contain the expected line
    assert any(expected_line in line for line in lines), f"Expected '{expected_line}' to be in {log_path}, but it was not found. Contents: {lines}"