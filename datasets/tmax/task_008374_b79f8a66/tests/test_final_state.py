# test_final_state.py

import os
import subprocess
import pytest

def test_failing_line_file():
    failing_line_path = "/home/user/failing_line.txt"
    assert os.path.isfile(failing_line_path), f"File {failing_line_path} does not exist."

    with open(failing_line_path, "r") as f:
        content = f.read().strip()

    expected_line = "2023-10-25 192.168.1.99 O'Connor LOGIN"
    assert content == expected_line, f"Expected {failing_line_path} to contain exactly '{expected_line}', but got '{content}'."

def test_output_log_exists_and_line_count():
    logs_path = "/home/user/data/logs.txt"
    output_path = "/home/user/output.log"

    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the pipeline?"

    with open(logs_path, "r") as f:
        input_lines = f.readlines()

    with open(output_path, "r") as f:
        output_lines = f.readlines()

    assert len(output_lines) == len(input_lines), (
        f"Output log has {len(output_lines)} lines, but input log has {len(input_lines)} lines. "
        "The pipeline must process all lines."
    )

def test_output_log_contains_correct_entry():
    output_path = "/home/user/output.log"
    expected_output_line = "2023-10-25 192.168.1.99 O'Connor UNKNOWN LOGIN"

    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read()

    assert expected_output_line in content, (
        f"Could not find the correctly processed line '{expected_output_line}' in {output_path}. "
        "Ensure the pipeline correctly handles single quotes and defaults to 'UNKNOWN' role."
    )

def test_pipeline_runs_successfully():
    script_path = "/home/user/pipeline.sh"
    logs_path = "/home/user/data/logs.txt"

    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run([script_path, logs_path], capture_output=True, text=True)

    assert result.returncode == 0, (
        f"Pipeline script failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )