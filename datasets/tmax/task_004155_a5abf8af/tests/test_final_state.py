# test_final_state.py

import os
import json
import subprocess
import pytest

def test_anomalies_json_exists_and_correct():
    """Check that anomalies.json is generated and contains the correct data."""
    file_path = "/home/user/anomalies.json"
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert isinstance(data, list), f"Expected a JSON array in {file_path}"
    assert len(data) == 1, f"Expected exactly 1 anomaly in {file_path}, found {len(data)}"

    anomaly = data[0]
    assert anomaly.get("timestamp") == "2023-10-01T10:05:00", "Incorrect timestamp for the anomaly."
    assert anomaly.get("worker_threads") == 50, "Incorrect worker_threads value for the anomaly."
    assert anomaly.get("z_score") == 1.79, f"Incorrect z_score, expected 1.79, got {anomaly.get('z_score')}"

def test_crontab_configured():
    """Check that the crontab is configured correctly for the user."""
    # Assuming tests run as root, we check the crontab of 'user'
    # If the tests run as 'user', `crontab -l` is sufficient. We will try `crontab -u user -l` first.
    try:
        result = subprocess.run(["crontab", "-u", "user", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        try:
            # Fallback if -u user fails (e.g., running as user already)
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
            crontab_output = result.stdout
        except subprocess.CalledProcessError:
            pytest.fail("Failed to retrieve crontab. Is it configured?")

    lines = crontab_output.strip().split('\n')
    found = False
    for line in lines:
        if line.startswith("*/5 * * * *") and "python3 /home/user/detect_anomalies.py" in line:
            found = True
            break

    assert found, "Crontab entry for detect_anomalies.py running every 5 minutes was not found."

def test_script_exists():
    """Check that the detect_anomalies.py script exists."""
    script_path = "/home/user/detect_anomalies.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"