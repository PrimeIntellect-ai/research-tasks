# test_final_state.py
import os
import re

def test_script_exists_and_executable():
    path = "/home/user/test_pipeline.sh"
    assert os.path.isfile(path), f"Script missing: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_clean_output_matches_expected():
    expected_path = "/home/user/expected_clean.csv"
    actual_path = "/home/user/clean_output.csv"

    assert os.path.isfile(actual_path), f"Output file missing: {actual_path}"

    with open(expected_path, 'r') as f:
        expected_lines = f.read().splitlines()

    with open(actual_path, 'r') as f:
        actual_lines = f.read().splitlines()

    assert len(actual_lines) == len(expected_lines), f"Line count mismatch: expected {len(expected_lines)}, got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"

def test_report_log_format():
    log_path = "/home/user/report.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()

    pattern = r"Benchmark complete\. 5 iterations took [0-9]*\.?[0-9]+ seconds\."
    assert re.search(pattern, content) is not None, f"Report log does not contain the correctly formatted benchmark string. Content found:\n{content}"