# test_final_state.py
import os
import subprocess
import socket
import urllib.request
import pytest

SCRIPT_PATH = "/home/user/setup_collector.sh"
CRON_SCRIPT = "/home/user/record_capacity.sh"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_port_8080_forwarding():
    # Execute the script to ensure it has run
    try:
        subprocess.run([SCRIPT_PATH], check=True, timeout=15)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {SCRIPT_PATH} failed: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {SCRIPT_PATH} timed out.")

    # Check if port 8080 is open and returns HTTP 200 (forwarded to python http server)
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/", timeout=3)
        assert req.getcode() == 200, "Port 8080 did not return HTTP 200, forwarding might be broken."
    except Exception as e:
        pytest.fail(f"Failed to connect to port 8080 or forwarder is not working: {e}")

def test_socat_idempotency():
    # Run the script a second time to test idempotency
    try:
        subprocess.run([SCRIPT_PATH], check=True, timeout=15)
    except Exception as e:
        pytest.fail(f"Second execution of {SCRIPT_PATH} failed, script might not be idempotent: {e}")

    # Count socat processes listening on 8080
    try:
        # Check process list for socat commands containing 8080
        p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE, text=True)
        stdout, _ = p1.communicate()

        socat_count = 0
        for line in stdout.splitlines():
            if "socat" in line and "8080" in line and "grep" not in line:
                socat_count += 1

        assert socat_count == 1, f"Expected exactly 1 socat process for port 8080, found {socat_count}."
    except Exception as e:
        pytest.fail(f"Failed to check socat processes: {e}")

def test_crontab_idempotency():
    # Check the user's crontab for exactly one occurrence of the script
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        # If crontab is empty or doesn't exist, it might return non-zero, but we expect it to exist
        output = result.stdout

        cron_count = 0
        for line in output.splitlines():
            if not line.strip().startswith("#") and CRON_SCRIPT in line:
                cron_count += 1

        assert cron_count == 1, f"Expected exactly 1 cron job entry for {CRON_SCRIPT}, found {cron_count}."
    except Exception as e:
        pytest.fail(f"Failed to read crontab: {e}")