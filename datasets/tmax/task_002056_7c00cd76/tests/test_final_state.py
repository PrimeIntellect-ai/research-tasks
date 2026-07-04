# test_final_state.py

import os
import subprocess
import time

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) >= 2, f"{report_path} must contain at least two lines."
    assert lines[0] == "REQ-103", f"Expected first line to be 'REQ-103', got '{lines[0]}'."
    assert lines[1] == "1.5", f"Expected second line to be '1.5', got '{lines[1]}'."

def test_test_suite_passes():
    test_suite_path = "/home/user/app/test_suite.py"
    assert os.path.isfile(test_suite_path), f"{test_suite_path} does not exist."

    result = subprocess.run(
        ["python3", test_suite_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"test_suite.py failed with error:\n{result.stderr}"
    assert "OK" in result.stdout, "test_suite.py did not print 'OK'."

def test_mre_execution():
    mre_path = "/home/user/mre.py"
    assert os.path.isfile(mre_path), f"{mre_path} does not exist."

    start_time = time.time()
    result = subprocess.run(
        ["python3", mre_path],
        capture_output=True,
        text=True,
        timeout=2.0
    )
    end_time = time.time()

    assert result.returncode == 0, f"mre.py failed to execute:\n{result.stderr}"

    execution_time = end_time - start_time
    assert execution_time < 1.0, f"mre.py took too long to execute ({execution_time:.2f} seconds), it should finish in under 1 second."

def test_processor_fix():
    processor_path = "/home/user/app/processor.py"
    assert os.path.isfile(processor_path), f"{processor_path} does not exist."

    with open(processor_path, "r") as f:
        content = f.read()

    # Check if the user implemented some form of NaN or Inf checking
    has_isnan = "isnan" in content
    has_isinf = "isinf" in content

    assert has_isnan or has_isinf, "processor.py does not seem to contain checks for NaN or Inf as required."