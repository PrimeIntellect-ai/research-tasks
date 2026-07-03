# test_final_state.py

import os
import json
import pytest

def test_diagnostic_summary_exists_and_correct():
    summary_path = "/home/user/diagnostic_summary.json"
    assert os.path.exists(summary_path), f"Diagnostic summary file missing: {summary_path}"

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    assert "valid" in data, "Key 'valid' missing in diagnostic_summary.json"
    assert "errors" in data, "Key 'errors' missing in diagnostic_summary.json"

    assert data["valid"] == 5, f"Expected 5 valid records, found {data['valid']}"
    assert data["errors"] == 0, f"Expected 0 error records, found {data['errors']}"

def test_app_log_untouched():
    log_file_path = "/home/user/data/app.log"
    assert os.path.exists(log_file_path), f"Log file missing: {log_file_path}"

    with open(log_file_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 5, "The log file /home/user/data/app.log appears to have been modified (line count changed)."
    assert "hello | world" in lines[2], "The log file /home/user/data/app.log appears to have been modified."

def test_process_logs_script_exists():
    script_file_path = "/home/user/process_logs.py"
    assert os.path.exists(script_file_path), f"Script file missing: {script_file_path}"