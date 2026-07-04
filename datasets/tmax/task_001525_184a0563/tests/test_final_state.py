# test_final_state.py

import os
import subprocess
import pytest

def test_run_ci_sh_exists_and_executable():
    script_path = "/home/user/run_ci.sh"
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_run_ci_execution_and_report():
    script_path = "/home/user/run_ci.sh"
    version_path = "/home/user/version.txt"
    report_path = "/home/user/ci_report.txt"

    # Read the expected version
    assert os.path.isfile(version_path), "version.txt is missing."
    with open(version_path, "r") as f:
        version = f.read().strip()

    # Remove the report if it exists to ensure the script creates it
    if os.path.exists(report_path):
        os.remove(report_path)

    # Run the CI script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_ci.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check the report
    assert os.path.isfile(report_path), f"The report file {report_path} was not created by run_ci.sh."
    with open(report_path, "r") as f:
        report_content = f.read().strip()

    expected_report = f"CI SUCCESS: {version}"
    assert report_content == expected_report, f"Expected report content '{expected_report}', but got '{report_content}'."

def test_parser_memory_leak_fixed():
    parser_path = "/home/user/parser"
    data_path = "/home/user/data.txt"

    assert os.path.isfile(parser_path), f"The compiled executable {parser_path} does not exist."
    assert os.access(parser_path, os.X_OK), f"The file {parser_path} is not executable."

    # Run valgrind to check for memory leaks
    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=1",
        parser_path,
        data_path
    ]
    result = subprocess.run(valgrind_cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Valgrind detected memory leaks or errors. Exit code: {result.returncode}.\nStderr: {result.stderr}"