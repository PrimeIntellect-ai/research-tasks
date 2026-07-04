# test_final_state.py

import os
import subprocess
import pytest

def test_build_script_fixed():
    build_path = "/home/user/pipeline_project/build.sh"
    assert os.path.isfile(build_path), f"Build script missing at {build_path}"
    with open(build_path, "r") as f:
        content = f.read()
    assert "req.txt" not in content, "Build script still contains the incorrect 'req.txt' reference."
    assert "requirements.txt" in content, "Build script does not contain the correct 'requirements.txt' reference."

def test_trace_log_content():
    trace_path = "/home/user/diagnostics/trace.log"
    assert os.path.isfile(trace_path), f"Trace log missing at {trace_path}"
    with open(trace_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = ["101", "102", "103", "104", "105", "106", "107", "108"]
    assert lines == expected_ids, f"Trace log contents do not match expected IDs. Got: {lines}"

def test_corrupted_rows_log_content():
    corrupted_path = "/home/user/diagnostics/corrupted_rows.log"
    assert os.path.isfile(corrupted_path), f"Corrupted rows log missing at {corrupted_path}"
    with open(corrupted_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_corrupted = ["104,CORRUPTED_DATA", "107,INVALID"]
    for expected in expected_corrupted:
        assert expected in lines, f"Expected corrupted row '{expected}' not found in {corrupted_path}"

def test_result_txt_content():
    result_path = "/home/user/diagnostics/result.txt"
    assert os.path.isfile(result_path), f"Result file missing at {result_path}"
    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "300", f"Result file does not contain the correct sum. Expected '300', got '{content}'"

def test_regression_test_exists_and_passes():
    test_path = "/home/user/pipeline_project/test_regression.py"
    assert os.path.isfile(test_path), f"Regression test file missing at {test_path}"

    with open(test_path, "r") as f:
        content = f.read()
    assert "test_corrupted_data_handling" in content, "Regression test file does not define 'test_corrupted_data_handling'"

    # Run pytest on the regression test file
    result = subprocess.run(
        ["pytest", test_path, "-v"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Regression test failed to run or did not pass.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert "test_corrupted_data_handling" in result.stdout, "The specific test 'test_corrupted_data_handling' was not executed by pytest."