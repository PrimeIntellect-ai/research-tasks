# test_final_state.py

import os
import pytest

def test_final_report_exists():
    report_path = "/home/user/final_report.txt"
    assert os.path.exists(report_path), f"The final report file {report_path} was not found."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

def test_final_report_content():
    report_path = "/home/user/final_report.txt"
    if not os.path.exists(report_path):
        pytest.fail(f"Cannot check content because {report_path} does not exist.")

    with open(report_path, "r") as f:
        content = f.read()

    # Define the expected lines based on the data and the required precision
    expected_lines = [
        "Filename: sensor_1.txt, Mean: 12.0000, Variance: 2.6667",
        "Filename: sensor_2.txt, Mean: 100000000.2000, Variance: 0.0067",
        "Filename: sensor 3.txt, Mean: 6.0000, Variance: 1.0000"
    ]

    for expected in expected_lines:
        assert expected in content, (
            f"Expected output line not found in {report_path}.\n"
            f"Missing: '{expected}'\n"
            f"This indicates either a failure to process a file (e.g. spaces in filename), "
            f"a crash on invalid data, or incorrect math calculations (precision issues)."
        )

def test_run_all_script_modifications():
    script_path = "/home/user/pipeline/run_all.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that the original buggy line is not present or has been modified
    assert "for f in $(find" not in content or "IFS=" in content or "while" in content or "-print0" in content, (
        "The run_all.sh script does not appear to correctly handle filenames with spaces. "
        "The naive 'for f in $(find ...)' approach is still present."
    )

def test_process_cpp_modifications():
    cpp_path = "/home/user/pipeline/process.cpp"
    assert os.path.exists(cpp_path), f"Source file {cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    # Check for double precision usage
    assert "double" in content, "The C++ program does not seem to use 'double' precision variables as required to fix the floating-point issue."

    # Check for exception handling or safer parsing
    assert "try" in content or "catch" in content or "stod" in content, (
        "The C++ program does not seem to contain exception handling (try/catch) "
        "or safer parsing to prevent crashes on invalid arguments."
    )