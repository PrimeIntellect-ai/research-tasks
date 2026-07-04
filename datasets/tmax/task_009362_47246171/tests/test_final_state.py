# test_final_state.py

import os
import re
import pytest

def test_anomalies_file_exists():
    assert os.path.isfile("/home/user/anomalies.txt"), "The file /home/user/anomalies.txt does not exist."

def test_anomalies_file_content():
    expected_line = "Anomaly detected at 1620000006: 61000 ms"
    with open("/home/user/anomalies.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 anomaly in output, but found {len(lines)} lines."
    assert lines[0] == expected_line, f"Expected output '{expected_line}', but got '{lines[0]}'."

def test_analyzer_executable_exists():
    assert os.path.isfile("/home/user/analyzer"), "The compiled executable /home/user/analyzer does not exist."
    assert os.access("/home/user/analyzer", os.X_OK), "The file /home/user/analyzer is not executable."

def test_analyzer_c_fixed_sum_sq():
    with open("/home/user/analyzer.c", "r") as f:
        content = f.read()

    # Check if sum_sq is no longer just an int, or is cast properly.
    # The most common fix is changing `int sum_sq` to `long long sum_sq` or `double sum_sq` or `long sum_sq`.
    # We can just check that sum_sq is not declared as exactly `int sum_sq = 0;` anymore without a cast,
    # but the output test is the strongest indicator of success.

    # Let's ensure the user didn't just hardcode the output.
    assert "1620000006" not in content, "The source code should not hardcode the expected output."
    assert "61000" not in content, "The source code should not hardcode the expected output."