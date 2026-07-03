# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_bug_report_content():
    report_path = "/home/user/bug_report.txt"
    assert os.path.isfile(report_path), f"Bug report file missing at {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected = "Faulty ID: BAD-999-LEAK"
    assert content == expected, f"Expected bug report to contain '{expected}', but got '{content}'"

def test_pytest_suite_passes():
    test_file = "/home/user/app/tests/test_consumer.py"
    assert os.path.isfile(test_file), f"Test file missing at {test_file}"

    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_consumer_memory_leak_fixed():
    # Insert app directory into sys.path to import consumer
    app_dir = "/home/user/app"
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)

    try:
        import consumer
    except ImportError as e:
        pytest.fail(f"Failed to import consumer.py: {e}")

    # Reset ERROR_HISTORY just in case
    consumer.ERROR_HISTORY = []

    # Test the edge case payload
    payload = '{"date": "2023/10/24"}'
    initial_len = len(consumer.ERROR_HISTORY)

    result = consumer.process_payload(payload)

    # The memory leak was caused by appending to ERROR_HISTORY on this format
    assert len(consumer.ERROR_HISTORY) == initial_len, "consumer.py still appends to ERROR_HISTORY for the YYYY/MM/DD format (memory leak not fixed)"

    # The parser should handle the alternative date format gracefully
    assert result == "2023-10-24T00:00:00", f"process_payload did not return the expected ISO format string for YYYY/MM/DD format, got: {result}"