# test_final_state.py

import os
import math

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read()

    # The expected standard deviation for 100000.1, 100000.2, 100000.3
    # Mean = 100000.2
    # Variance = ((100000.1 - 100000.2)^2 + (100000.2 - 100000.2)^2 + (100000.3 - 100000.2)^2) / 3
    # Variance = (0.01 + 0 + 0.01) / 3 = 0.02 / 3 = 0.006666...
    # Stddev = sqrt(0.006666...) = 0.081649658...
    # Formatted to 4 decimal places: 0.0816

    expected = "0.0816"
    assert content.strip() == expected, f"Expected content '{expected}', but got '{content.strip()}'"
    assert content.endswith("\n"), f"File {result_path} must have a trailing newline."

def test_log_analyzer_fixed():
    go_file = "/home/user/log_analyzer.go"
    assert os.path.isfile(go_file), f"File {go_file} is missing."

    with open(go_file, "r") as f:
        content = f.read()

    # The task requires upgrading float32 to float64
    assert "float64" in content, "The script does not seem to have been upgraded to use float64."
    assert "float32" not in content, "The script still contains float32 types, which cause precision loss."