# test_final_state.py
import os
import pytest

def test_daemon_compiled():
    daemon_path = "/home/user/app/daemon/dpi_daemon"
    assert os.path.isfile(daemon_path), f"DPI Daemon executable not found at {daemon_path}. Did the build fail?"
    assert os.access(daemon_path, os.X_OK), f"DPI Daemon at {daemon_path} is not executable."

def test_parsed_tlvs_metric():
    log_file = "/home/user/app/aggregator/parsed_tlvs.log"
    assert os.path.isfile(log_file), f"Aggregator log file not found at {log_file}. Did the services run and process packets?"

    with open(log_file, 'r') as f:
        lines = f.readlines()

    metric_value = len(lines)
    threshold = 4900

    assert metric_value >= threshold, (
        f"Expected at least {threshold} successfully parsed TLV records, "
        f"but found {metric_value}. The daemon likely hung or crashed "
        f"due to the integer overflow bug before processing the full stream."
    )