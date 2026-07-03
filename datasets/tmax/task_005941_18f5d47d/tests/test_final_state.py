# test_final_state.py

import os
import json
import subprocess
import pytest

def test_normalized_logs_exists_and_content():
    """Verify the normalized logs file exists and contains the correct JSON data."""
    output_path = "/home/user/data/normalized_logs.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 5, f"Expected 5 lines in {output_path}, found {len(lines)}."

    expected_data = [
        {"id": 1, "temp_c": 40.0, "notes": "normal log"},
        {"id": 2, "temp_c": 10.0, "notes": "malformed \u0001 sequence"},
        {"id": 3, "temp_c": 30.0, "notes": "all good here"},
        {"id": 4, "temp_c": 0.0, "notes": "another \u0001 issue"},
        {"id": 5, "temp_c": 37.0, "notes": "human body temp"},
    ]

    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

        expected_obj = expected_data[i]

        assert "temp_f" not in obj, f"Line {i+1} still contains 'temp_f'."
        assert "temp_c" in obj, f"Line {i+1} is missing 'temp_c'."
        assert "id" in obj, f"Line {i+1} is missing 'id'."
        assert "notes" in obj, f"Line {i+1} is missing 'notes'."

        assert obj["id"] == expected_obj["id"], f"Line {i+1} has incorrect 'id'."
        assert abs(obj["temp_c"] - expected_obj["temp_c"]) < 1e-5, f"Line {i+1} has incorrect 'temp_c'."
        assert obj["notes"] == expected_obj["notes"], f"Line {i+1} has incorrect 'notes'."

def test_run_pipeline_script():
    """Verify the run_pipeline.sh script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_rust_binary_exists():
    """Verify the Rust application was built in release mode."""
    binary_path = "/home/user/log_processor/target/release/log_processor"
    assert os.path.isfile(binary_path), f"Rust release binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Rust release binary {binary_path} is not executable."

def test_cron_job_installed():
    """Verify the cron job is installed with the correct schedule."""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it installed?")

    expected_cron = "30 2 * * * /home/user/run_pipeline.sh"

    # Check if any line in crontab matches the expected schedule and command
    matching_lines = [line.strip() for line in crontab_output.strip().split('\n') if expected_cron in line]
    assert len(matching_lines) > 0, f"Crontab does not contain the expected job: '{expected_cron}'"