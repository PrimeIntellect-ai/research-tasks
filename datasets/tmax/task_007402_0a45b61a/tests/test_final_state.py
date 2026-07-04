# test_final_state.py

import os
import json
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_etl_script():
    """Run the student's ETL bash script before checking the state."""
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_etl.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_venv_created():
    """Test that the virtual environment was created."""
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} does not exist."
    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_bin) or os.path.isfile(python_bin + "3"), "Python executable not found in the virtual environment."

def test_output_file_exists():
    """Test that the output.jsonl file was created."""
    output_path = "/home/user/output.jsonl"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

def test_output_file_content():
    """Test that the output.jsonl file contains the correct processed data."""
    output_path = "/home/user/output.jsonl"

    expected_data = [
        {"user_id": 1, "name": "Alice", "age": 25.0, "total_amount": 150.5},
        {"user_id": 2, "name": "Bob", "age": 30.0, "total_amount": 200.0},
        {"user_id": 5, "name": "Eve", "age": 30.0, "total_amount": 75.25}
    ]

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_data), f"Expected {len(expected_data)} lines in output.jsonl, but found {len(lines)}."

    for i, (expected, line) in enumerate(zip(expected_data, lines)):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in output.jsonl is not valid JSON: {line}")

        assert "user_id" in parsed, f"Line {i+1} missing 'user_id'"
        assert "name" in parsed, f"Line {i+1} missing 'name'"
        assert "age" in parsed, f"Line {i+1} missing 'age'"
        assert "total_amount" in parsed, f"Line {i+1} missing 'total_amount'"

        assert parsed["user_id"] == expected["user_id"], f"Line {i+1}: expected user_id {expected['user_id']}, got {parsed['user_id']}"
        assert parsed["name"] == expected["name"], f"Line {i+1}: expected name '{expected['name']}', got '{parsed['name']}'"
        assert float(parsed["age"]) == expected["age"], f"Line {i+1}: expected age {expected['age']}, got {parsed['age']}"
        assert float(parsed["total_amount"]) == expected["total_amount"], f"Line {i+1}: expected total_amount {expected['total_amount']}, got {parsed['total_amount']}"