# test_final_state.py
import os
import subprocess
import pytest

def test_analyzer_cpp_exists():
    assert os.path.isfile("/home/user/analyzer.cpp"), "Missing C++ source file: /home/user/analyzer.cpp"

def test_analyzer_executable_exists():
    assert os.path.isfile("/home/user/analyzer"), "Missing compiled executable: /home/user/analyzer"
    assert os.access("/home/user/analyzer", os.X_OK), "/home/user/analyzer is not executable"

def test_expect_script_exists():
    assert os.path.isfile("/home/user/run_analysis.exp"), "Missing expect script: /home/user/run_analysis.exp"

def test_expect_script_functionality():
    report_path = "/home/user/capacity_report.txt"
    if os.path.exists(report_path):
        os.remove(report_path)

    try:
        subprocess.run(["expect", "/home/user/run_analysis.exp"], check=True, timeout=10)
    except subprocess.CalledProcessError:
        pytest.fail("The expect script /home/user/run_analysis.exp failed to execute successfully.")
    except subprocess.TimeoutExpired:
        pytest.fail("The expect script /home/user/run_analysis.exp timed out.")

    assert os.path.isfile(report_path), f"The expect script did not create {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "Backend 10.0.0.10 exceeded with 15500 bytes.",
        "Backend 10.0.0.11 exceeded with 20000 bytes.",
        "Backend 10.0.0.12 exceeded with 15500 bytes.",
        "Backend 10.0.0.13 exceeded with 17000 bytes."
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {report_path}, but got {len(content)}. Content: {content}"

    for expected in expected_lines:
        assert expected in content, f"Expected line '{expected}' not found in {report_path}"

    for line in content:
        assert line.startswith("Backend"), f"Found unexpected line in {report_path} that does not start with 'Backend': {line}"