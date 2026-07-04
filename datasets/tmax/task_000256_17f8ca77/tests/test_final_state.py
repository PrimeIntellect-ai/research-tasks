# test_final_state.py
import os
import subprocess
import pytest

def test_final_metric_file():
    file_path = "/home/user/final_metric.txt"
    assert os.path.exists(file_path), f"File missing: {file_path}"
    assert os.path.isfile(file_path), f"Not a file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_value = "11500000000000000000"
    assert content == expected_value, f"Expected {expected_value} in {file_path}, but got {content}"

def test_script_execution():
    script_path = "/home/user/calculate_metrics.sh"
    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    try:
        result = subprocess.run([script_path], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with error: {e.stderr}")

    expected_value = "11500000000000000000"
    # The script might output other things, but the last line or the only line should be the total
    lines = [line for line in output.split('\n') if line.strip()]
    assert lines, "Script produced no output"
    assert lines[-1] == expected_value, f"Expected script to output {expected_value}, but got {lines[-1]}"