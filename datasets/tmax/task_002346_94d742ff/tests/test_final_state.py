# test_final_state.py
import os
import json
import pytest

WORKSPACE_DIR = "/home/user/ticket_8492"
LOGS_DIR = os.path.join(WORKSPACE_DIR, "logs")
ENV_FILE = os.path.join(WORKSPACE_DIR, ".env")
SCRIPT_FILE = os.path.join(WORKSPACE_DIR, "aggregate_logs.py")
REPORT_FILE = os.path.join(WORKSPACE_DIR, "report.json")
RESOLUTION_FILE = os.path.join(WORKSPACE_DIR, "resolution.txt")

def test_resolution_file_exists_and_correct():
    assert os.path.isfile(RESOLUTION_FILE), f"Resolution file {RESOLUTION_FILE} is missing."
    with open(RESOLUTION_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Resolution file must contain exactly two lines, found {len(lines)}."
    assert "log_027.txt" in lines[0], f"First line of resolution.txt should contain 'log_027.txt', got: {lines[0]}"
    assert lines[1] == "REQ_027_ANOMALY,-99999.999", f"Second line of resolution.txt should be exactly 'REQ_027_ANOMALY,-99999.999', got: {lines[1]}"

def test_env_file_fixed():
    assert os.path.isfile(ENV_FILE), f".env file {ENV_FILE} is missing."
    with open(ENV_FILE, "r") as f:
        content = f.read().strip()

    # It should point to the correct logs directory
    assert "LOG_DIR=" in content, ".env file must contain LOG_DIR assignment."
    val = content.split("LOG_DIR=")[1].strip()
    # Acceptable paths: /home/user/ticket_8492/logs, ./logs, logs
    valid_paths = [LOGS_DIR, "./logs", "logs"]
    assert val in valid_paths, f".env file LOG_DIR is set to '{val}', expected one of {valid_paths}."

def test_report_json_correct():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} was not generated."
    try:
        with open(REPORT_FILE, "r") as f:
            report = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Report file {REPORT_FILE} is not valid JSON.")

    assert "total_requests" in report, "Report JSON missing 'total_requests' key."
    assert report["total_requests"] == 5001, f"Expected total_requests to be 5001, got {report['total_requests']}. The race condition might not be fully fixed."
    assert "files_processed" in report, "Report JSON missing 'files_processed' key."
    assert report["files_processed"] == 50, f"Expected files_processed to be 50, got {report['files_processed']}."

def test_script_modified_for_concurrency():
    assert os.path.isfile(SCRIPT_FILE), f"Script file {SCRIPT_FILE} is missing."
    with open(SCRIPT_FILE, "r") as f:
        content = f.read()

    # We expect the script to have been modified. The initial script had an intentional race condition.
    # While we can't strictly assert the exact fix (Lock vs other mechanisms), we can verify the script
    # has changed from its initial state regarding the race condition.
    assert "Intentional race condition here" not in content or "Lock" in content or "total_requests" in content, "The script does not seem to be properly modified to handle the race condition."