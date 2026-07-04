# test_final_state.py

import os
import pytest

def test_venv_exists():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} is missing."
    assert os.path.isfile(os.path.join(venv_path, "bin", "python")), "Python executable missing in venv."

def test_fitter_script_exists():
    fitter_path = "/home/user/fitter.py"
    assert os.path.isfile(fitter_path), f"Fitter script {fitter_path} is missing."

def test_run_tests_script_exists_and_executable():
    script_path = "/home/user/run_tests.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

def test_regression_report_exists():
    report_path = "/home/user/regression_report.log"
    assert os.path.isfile(report_path), f"Regression report {report_path} is missing."

def test_regression_report_content():
    report_path = "/home/user/regression_report.log"
    assert os.path.isfile(report_path), f"Regression report {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "sensor_1: PASS",
        "sensor_2: FAIL",
        "sensor_3: PASS"
    ]

    assert lines == expected_lines, (
        f"Regression report contents do not match expected.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(lines)}"
    )