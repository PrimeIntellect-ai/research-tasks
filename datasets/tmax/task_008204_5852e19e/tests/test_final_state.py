# test_final_state.py
import os
import subprocess
import pytest

def test_cpp_file_exists():
    assert os.path.isfile('/home/user/etl_pipeline.cpp'), "/home/user/etl_pipeline.cpp does not exist."

def test_bash_script_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_pipeline_execution_and_output():
    script_path = '/home/user/run_pipeline.sh'

    # Execute the pipeline script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {script_path} failed.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check if executable was created
    assert os.path.isfile('/home/user/etl.out'), "/home/user/etl.out was not created by the bash script."

    # Check if summary.csv was created
    summary_path = '/home/user/summary.csv'
    assert os.path.isfile(summary_path), f"{summary_path} was not generated."

    expected_output = [
        "S-001,26.50",
        "S-002,11.00",
        "S-004,49.90",
        "S-005,-13.33"
    ]

    with open(summary_path, 'r') as f:
        actual_output = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert actual_output == expected_output, (
        f"The content of {summary_path} is incorrect.\n"
        f"Expected:\n{expected_output}\n"
        f"Got:\n{actual_output}"
    )