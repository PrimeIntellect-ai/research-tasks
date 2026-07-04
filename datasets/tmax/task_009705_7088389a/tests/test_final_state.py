# test_final_state.py

import os
import subprocess
import pytest

def test_process_graph_script_exists():
    assert os.path.isfile("/home/user/process_graph.sh"), "/home/user/process_graph.sh does not exist."

def test_validate_script_exists():
    assert os.path.isfile("/home/user/validate.sh"), "/home/user/validate.sh does not exist."

def test_process_graph_execution_and_outputs():
    # Run the process_graph.sh script
    result = subprocess.run(["bash", "/home/user/process_graph.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"process_graph.sh failed to execute. stderr: {result.stderr}"

    # Check if graph.db was created
    assert os.path.isfile("/home/user/graph.db"), "/home/user/graph.db was not created."

    # Check the contents of summary.csv
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"{summary_path} was not created."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_content = "metric_name,value\ntotal_active_capacity,610\nshortest_path_cost,50"

    # Normalize line endings for comparison
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert content_lines == expected_lines, f"Content of {summary_path} is incorrect. Got:\n{content}\nExpected:\n{expected_content}"

def test_validate_script_execution():
    # Run the validate.sh script
    result = subprocess.run(["bash", "/home/user/validate.sh"], capture_output=True, text=True)

    assert result.returncode == 0, f"validate.sh returned non-zero exit code: {result.returncode}. stderr: {result.stderr}"
    assert result.stdout.strip() == "VALID", f"validate.sh did not print 'VALID'. Got: {result.stdout.strip()}"