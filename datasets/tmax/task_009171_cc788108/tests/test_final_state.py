# test_final_state.py

import os
import stat
import json
import subprocess
import pytest

def test_directories_exist():
    directories = [
        "/home/user/incoming",
        "/home/user/processed",
        "/home/user/pipeline"
    ]
    for directory in directories:
        assert os.path.isdir(directory), f"Directory {directory} does not exist."

def test_scripts_exist_and_executable():
    process_py = "/home/user/pipeline/process.py"
    run_sh = "/home/user/pipeline/run.sh"

    assert os.path.isfile(process_py), f"Python script {process_py} does not exist."
    assert os.path.isfile(run_sh), f"Wrapper script {run_sh} does not exist."

    st = os.stat(run_sh)
    assert bool(st.st_mode & stat.S_IXUSR), f"Wrapper script {run_sh} is not executable."

def test_cron_job_configured():
    try:
        # Check crontab for user 'user'
        result = subprocess.run(['crontab', '-u', 'user', '-l'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab for user 'user'.")

    expected_cron = "*/10 * * * * /home/user/pipeline/run.sh"
    # Check if any line in the crontab matches the expected command and schedule
    lines = [line.strip() for line in crontab_content.splitlines() if line.strip() and not line.startswith('#')]

    match_found = any(expected_cron in line for line in lines)
    assert match_found, f"Expected cron job '{expected_cron}' not found in user's crontab."

def test_incoming_directory_empty():
    incoming_dir = "/home/user/incoming"
    assert os.path.isdir(incoming_dir), f"Directory {incoming_dir} does not exist."
    files = os.listdir(incoming_dir)
    assert len(files) == 0, f"Expected {incoming_dir} to be empty, but found: {files}"

def test_processed_files_moved():
    processed_dir = "/home/user/processed"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."
    files = set(os.listdir(processed_dir))
    expected_files = {"batch1.csv", "batch2.csv"}
    assert expected_files.issubset(files), f"Expected files {expected_files} to be in {processed_dir}, but found {files}"

def test_word_frequencies_json():
    json_path = "/home/user/pipeline/word_frequencies.json"
    assert os.path.isfile(json_path), f"JSON file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected_counts = {
        "the": 2,
        "battery": 1,
        "life": 1,
        "is": 1,
        "terrible": 2,
        "love": 2,
        "screen": 2,
        "very": 1,
        "bright": 2,
        "will": 1,
        "return": 1,
        "it": 1
    }

    assert data == expected_counts, f"Word frequencies do not match expected values. Got: {data}"