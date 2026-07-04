# test_final_state.py

import os
import re
import subprocess
import requests
import pytest

def test_makefile_fixed():
    """Check that the Makefile contains the -pthread flag."""
    makefile_path = "/app/sys-exporter-1.2.0/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-pthread" in content, "Makefile is still missing the -pthread flag."

def test_main_cpp_fixed():
    """Check that main.cpp has the typo fixed."""
    main_cpp_path = "/app/sys-exporter-1.2.0/main.cpp"
    assert os.path.isfile(main_cpp_path), f"{main_cpp_path} is missing."
    with open(main_cpp_path, "r") as f:
        content = f.read()
    assert "TARGET_DIR" in content, "main.cpp does not contain the corrected 'TARGET_DIR'."
    assert "TARGT_DIR" not in content, "main.cpp still contains the 'TARGT_DIR' typo."

def test_cron_job_configured():
    """Check that the user has the correct cron job configured."""
    try:
        result = subprocess.run(
            ["crontab", "-l", "-u", "user"],
            capture_output=True,
            text=True,
            check=True
        )
        crontab_content = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab for 'user'. Error: {e.stderr}")

    expected_cron = r"@reboot\s+/home/user/start_exporter\.sh"
    assert re.search(expected_cron, crontab_content), "Cron job for @reboot /home/user/start_exporter.sh is missing or incorrect."

def test_profile_exports():
    """Check that .profile contains the required exports."""
    profile_path = "/home/user/.profile"
    assert os.path.isfile(profile_path), f"{profile_path} is missing."

    with open(profile_path, "r") as f:
        content = f.read()

    assert re.search(r"export\s+SERVER_PORT=8080\b", content), "export SERVER_PORT=8080 is missing in .profile."
    assert re.search(r"export\s+TARGET_DIR=/home/user/mnt_data\b", content), "export TARGET_DIR=/home/user/mnt_data is missing in .profile."

def test_http_endpoint_serves_data():
    """Check that the sys-exporter service is running and serving the correct data."""
    url = "http://127.0.0.1:8080/system_stats.json"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the sys-exporter service at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."

    expected_data = {"status": "ok", "cpu_usage": 42.5, "memory": "16GB"}
    try:
        actual_data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert actual_data == expected_data, f"Expected JSON {expected_data}, got {actual_data}."