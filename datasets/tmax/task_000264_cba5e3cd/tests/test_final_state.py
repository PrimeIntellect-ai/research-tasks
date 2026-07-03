# test_final_state.py

import os
import pytest

def test_duplicate_report_content():
    report_path = "/home/user/duplicate_report.txt"
    assert os.path.exists(report_path), f"Report not found at {report_path}."

    expected_report = """Audit Report
============
Total Retried Jobs: 2
Affected Transactions:
- TXN_003 (Job: JOB_B, Amount: 200)
- TXN_005 (Job: JOB_D, Amount: 500)"""

    with open(report_path, "r") as f:
        actual_report = f.read().strip()

    assert actual_report == expected_report.strip(), f"Report content mismatch. Got:\n{actual_report}"

def test_pipeline_log_exists_and_not_empty():
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Pipeline log not found at {log_path}."

    with open(log_path, "r") as f:
        logs = f.read()

    assert len(logs.strip()) > 0, "Pipeline log is empty."

def test_script_uses_multiprocessing():
    script_path = "/home/user/analyze_retries.py"
    assert os.path.exists(script_path), f"Python script not found at {script_path}."

    with open(script_path, "r") as f:
        script_content = f.read()

    assert "multiprocessing" in script_content, "Script does not use multiprocessing as required."