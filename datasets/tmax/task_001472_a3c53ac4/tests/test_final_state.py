# test_final_state.py

import os
import pytest

def test_stability_report_exists_and_content():
    report_path = "/home/user/stability_report.csv"
    assert os.path.isfile(report_path), f"Expected report file {report_path} does not exist."

    expected_content = (
        "dt,final_value,status\n"
        "0.2,0.000000,STABLE\n"
        "0.8,0.002177,STABLE\n"
        "1.2,14.757891,UNSTABLE\n"
        "2.0,-243.000000,UNSTABLE\n"
        "REGRESSION_CHECK:PASS\n"
    )

    with open(report_path, "r") as f:
        content = f.read()

    # Strip trailing whitespace/newlines from the file content and expected content for a robust comparison
    assert content.strip() == expected_content.strip(), (
        f"Content of {report_path} does not match expected.\n"
        f"Expected:\n{expected_content.strip()}\n\n"
        f"Got:\n{content.strip()}"
    )

def test_run_tests_script_exists_and_executable():
    script_path = "/home/user/run_tests.sh"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Expected script {script_path} to be executable."