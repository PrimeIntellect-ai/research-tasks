# test_final_state.py

import os
import pytest

def test_merger_executable_exists():
    path = "/home/user/merger"
    assert os.path.isfile(path), f"File {path} does not exist. Did you compile the Rust code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_run_tests_sh_exists():
    path = "/home/user/run_tests.sh"
    assert os.path.isfile(path), f"File {path} does not exist. Did you create the Bash script?"

def test_test_report_log_contents():
    path = "/home/user/test_report.log"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the tests?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "[PASS] case1",
        "[PASS] case2"
    ]

    assert lines == expected_lines, f"Contents of {path} are incorrect. Expected {expected_lines}, got {lines}."

def test_output_txt_generated():
    cases = ["case1", "case2"]
    for case in cases:
        output_path = f"/home/user/tests/{case}/output.txt"
        expected_path = f"/home/user/tests/{case}/expected.txt"

        assert os.path.isfile(output_path), f"File {output_path} was not generated."

        with open(output_path, "r") as f:
            output_content = f.read().strip()

        with open(expected_path, "r") as f:
            expected_content = f.read().strip()

        assert output_content == expected_content, f"Output for {case} does not match expected."