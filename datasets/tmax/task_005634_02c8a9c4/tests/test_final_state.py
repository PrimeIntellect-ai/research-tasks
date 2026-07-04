# test_final_state.py

import os
import json
import pytest

def test_fuzzer_and_logs():
    """Verify fuzzer.py exists and 50 log files with 1000 lines each are generated."""
    fuzzer_path = "/home/user/fuzzer.py"
    assert os.path.isfile(fuzzer_path), f"Fuzzer script {fuzzer_path} is missing."

    logs_dir = "/home/user/logs"
    assert os.path.isdir(logs_dir), f"Logs directory {logs_dir} is missing."

    log_files = [f for f in os.listdir(logs_dir) if f.endswith(".log")]
    assert len(log_files) == 50, f"Expected 50 log files in {logs_dir}, found {len(log_files)}."

    for log_file in log_files:
        log_path = os.path.join(logs_dir, log_file)
        with open(log_path, "r") as f:
            lines = f.readlines()
        assert len(lines) == 1000, f"Expected 1000 lines in {log_file}, found {len(lines)}."

def test_summary_json():
    """Verify summary.json exists and the total count is exactly 50000."""
    summary_path = "/home/user/summary.json"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} is missing."

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    assert "ERROR" in data and "WARN" in data and "INFO" in data, "JSON must contain ERROR, WARN, and INFO keys."
    total = sum(data.values())
    assert total == 50000, f"Expected 50000 total logs, got {total}."

def test_ticket_resolution():
    """Verify ticket_resolution.txt contains the exact ERROR count from summary.json."""
    summary_path = "/home/user/summary.json"
    assert os.path.isfile(summary_path), "Cannot verify resolution without summary.json."

    with open(summary_path, "r") as f:
        data = json.load(f)

    res_path = "/home/user/ticket_resolution.txt"
    assert os.path.isfile(res_path), f"Resolution file {res_path} is missing."

    with open(res_path, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Content of {res_path} is not a valid integer."
    res_error = int(content)
    assert res_error == data["ERROR"], f"Expected {data['ERROR']} in resolution, got {res_error}."

def test_log_aggregator_fixed():
    """Verify log_aggregator.py uses a Lock to fix the race condition."""
    script_path = "/home/user/log_aggregator.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "Lock" in content, "No thread lock found in the fixed script."
    if "time.sleep" in content:
        assert "acquire" in content or "with " in content, "Race condition doesn't seem to be mitigated (Lock not acquired)."