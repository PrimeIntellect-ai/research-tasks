# test_final_state.py
import os
import json
import subprocess
import pytest

def test_bad_commit_hash_correct():
    expected_file = "/tmp/expected_bad_commit.txt"
    student_file = "/home/user/bad_commit.txt"

    assert os.path.exists(student_file), f"File {student_file} does not exist."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(student_file, "r") as f:
        student_hash = f.read().strip()

    assert student_hash == expected_hash, f"Incorrect bad commit hash. Expected {expected_hash}, got {student_hash}."

def test_script_fixed_and_outputs_valid_json():
    script_path = "/home/user/telemetry_repo/process_telemetry.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    cmd = ["python3", script_path, '{"timestamp": 1690000000.123456, "value": 42.5}']
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    try:
        output_data = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        pytest.fail(f"Script output is not valid JSON.\nOutput: {result.stdout}")

    assert "time" in output_data, "Output JSON is missing 'time' key."
    assert "value" in output_data, "Output JSON is missing 'value' key."
    assert "delay" in output_data, "Output JSON is missing 'delay' key."
    assert output_data["value"] == 42.5, f"Expected value 42.5, got {output_data['value']}."