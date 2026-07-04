# test_final_state.py

import os
import json
import subprocess
import requests
import pytest

def test_services_running_and_configured():
    """
    Tests that Nginx, Flask, and Redis are correctly configured and running.
    The health endpoint should return 200 OK and {"status": "ok"}.
    """
    try:
        res = requests.get('http://127.0.0.1:8080/health', timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the health endpoint. Is Nginx running on port 8080? Error: {e}")

    assert res.status_code == 200, f"Expected status code 200, got {res.status_code}"

    try:
        data = res.json()
    except ValueError:
        pytest.fail("Health endpoint did not return valid JSON.")

    assert data == {"status": "ok"}, f"Expected health endpoint to return {{'status': 'ok'}}, got {data}"

def test_disk_usage_metric():
    """
    Tests that the total disk usage of /app/data/artifacts/ is <= 210000 KB.
    This verifies that duplicate files were successfully replaced with hard links.
    """
    artifacts_dir = "/app/data/artifacts/"
    assert os.path.exists(artifacts_dir), f"Directory {artifacts_dir} does not exist."

    try:
        out = subprocess.check_output(f"du -sk {artifacts_dir}", shell=True, text=True)
        size_kb = int(out.split()[0])
    except Exception as e:
        pytest.fail(f"Failed to compute disk usage for {artifacts_dir}. Error: {e}")

    threshold = 210000
    assert size_kb <= threshold, (
        f"Disk usage {size_kb} KB exceeded threshold of {threshold} KB. "
        "Deduplication via hard links was not completely successful."
    )

def test_curate_script_exists():
    """
    Verifies that the curation script was created at the specified path.
    """
    script_path = "/home/user/curate.py"
    assert os.path.isfile(script_path), f"Curation script {script_path} is missing."

def test_backup_index_exists_and_valid():
    """
    Verifies that the backup index JSON file was created and contains valid data.
    """
    index_path = "/app/data/backup_index.json"
    assert os.path.isfile(index_path), f"Backup index file {index_path} is missing."

    try:
        with open(index_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Backup index file {index_path} does not contain valid JSON.")

    assert isinstance(data, dict), f"Expected backup index to be a JSON dictionary, got {type(data).__name__}."
    assert len(data) > 0, "Backup index JSON dictionary is empty."

    # Check that the values look like SHA-256 hashes (64 hex characters)
    for path, file_hash in data.items():
        assert isinstance(path, str), f"Expected path to be a string, got {type(path).__name__}."
        assert isinstance(file_hash, str) and len(file_hash) == 64, (
            f"Expected hash to be a 64-character string (SHA-256), got '{file_hash}' for path '{path}'."
        )