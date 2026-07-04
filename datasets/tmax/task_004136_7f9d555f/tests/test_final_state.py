# test_final_state.py

import os
import subprocess
import pytest

CRASH_URL = "https://this-is-a-very-long-url-that-will-cause-a-buffer-overflow.com/ping"

EXPECTED_URLS = {
    "http://example.com/api/v1/health",
    "https://internal-service.local/ping",
    "https://this-is-a-very-long-url-that-will-cause-a-buffer-overflow.com/ping",
    "http://localhost:8080/metrics"
}

def test_crash_cause_file():
    path = "/home/user/crash_cause.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == CRASH_URL, f"File {path} does not contain the correct crashing URL."

def test_recovered_urls_file():
    path = "/home/user/recovered_urls.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert set(lines) == EXPECTED_URLS, f"File {path} does not contain the exact expected URLs."
    assert len(lines) == len(EXPECTED_URLS), f"File {path} contains duplicate or incorrect number of URLs."

def test_uptime_monitor_script_execution():
    script_path = "/home/user/uptime-monitor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    try:
        result = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out during execution.")

    assert result.returncode == 0, (
        f"Script {script_path} failed with return code {result.returncode}.\n"
        f"Stderr: {result.stderr}"
    )

    expected_skip_msg = f"Skipped: {CRASH_URL}"
    assert expected_skip_msg in result.stdout, (
        f"Script output did not contain the expected skip message: '{expected_skip_msg}'\n"
        f"Stdout: {result.stdout}"
    )