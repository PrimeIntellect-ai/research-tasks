# test_final_state.py

import os
import pytest

def test_report_file():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) >= 2, f"Report file {report_path} must contain at least two lines."
    assert lines[0] == "042.dat", f"Line 1 of report.txt should be '042.dat', got '{lines[0]}'."
    assert lines[1] == "100", f"Line 2 of report.txt should be '100', got '{lines[1]}'."

def test_processed_log():
    log_path = "/home/user/service/processed.log"
    assert os.path.isfile(log_path), f"Processed log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 100, f"Expected 100 lines in {log_path}, got {len(lines)}. The Go program may still be crashing or was not run after fixing."

    # Verify that the poison pill was successfully processed
    poison_pill_entry = "/home/user/payloads/042.dat"
    assert poison_pill_entry in lines, f"Log file does not contain {poison_pill_entry}. The program might have skipped it instead of processing it correctly."

def test_go_source_modified():
    go_source = "/home/user/service/processor.go"
    assert os.path.isfile(go_source), f"Go source file {go_source} is missing."

    with open(go_source, "r") as f:
        content = f.read()

    # The original file had `i < len(data)`. We don't check for exact fix syntax, 
    # but we can ensure the file is still present and the processed log indicates the fix is effective.
    assert "package main" in content, "Go source does not contain 'package main'."
    assert "func processPayload" in content, "Go source does not contain processPayload function."