# test_final_state.py

import os
import json
import stat
import re
import subprocess
import pytest

def test_process_math_script_exists():
    path = "/home/user/process_math.py"
    assert os.path.isfile(path), f"Python script {path} does not exist."

def test_run_pipeline_script_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Bash script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {path} is not executable."

def test_cron_schedule_content():
    path = "/home/user/cron_schedule.txt"
    assert os.path.isfile(path), f"Cron schedule file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    # Check for 30 2 * * *
    # It might have user specified if it's a system crontab or just the command
    assert re.search(r"^30\s+2\s+\*\s+\*\s+\*", content, re.MULTILINE), f"Cron schedule {path} does not contain the correct time expression '30 2 * * *'."
    assert "/home/user/run_pipeline.sh" in content, f"Cron schedule {path} does not contain the command '/home/user/run_pipeline.sh'."

def test_pipeline_execution_and_output():
    # Execute the pipeline to ensure it works and generates the file
    script_path = "/home/user/run_pipeline.sh"

    # Remove the backup file if it exists to verify the script actually copies it
    backup_path = "/archive/remote_backup/grouped.json"
    if os.path.exists(backup_path):
        os.remove(backup_path)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.isfile(backup_path), f"Pipeline script did not create or copy the file to {backup_path}."

    with open(backup_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {backup_path} does not contain valid JSON.")

    expected_data = {
        "0": [1, 6],
        "1": [2],
        "3": [3, 4, 5],
        "5": [8],
        "8": [7],
        "10": [9]
    }

    # JSON keys are strings
    assert isinstance(data, dict), "JSON root must be a dictionary."

    # Convert keys to strings for expected data just in case
    expected_str_keys = {str(k): v for k, v in expected_data.items()}

    # Check if the parsed data matches expected
    for k, v in expected_str_keys.items():
        assert k in data, f"Key '{k}' missing from JSON output."
        assert data[k] == v, f"Values for key '{k}' do not match. Expected {v}, got {data[k]}."

    for k in data.keys():
        assert k in expected_str_keys, f"Unexpected key '{k}' found in JSON output."