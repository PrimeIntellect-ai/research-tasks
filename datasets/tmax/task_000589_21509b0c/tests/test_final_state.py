# test_final_state.py

import os
import time
import json
import subprocess
import pytest

def test_solution_ready():
    assert os.path.exists("/home/user/solution_ready.txt"), "Agent did not finish: /home/user/solution_ready.txt is missing"

def test_acls_correct():
    try:
        acl_output = subprocess.check_output(["getfacl", "/home/user/app_logs"]).decode()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to get ACLs for /home/user/app_logs: {e}")

    assert "default:user::r--" in acl_output or "default:user:user:r--" in acl_output, "Default ACLs not set correctly on /home/user/app_logs"

def test_service_performance_and_correctness():
    metrics_file = "/home/user/metrics.json"

    # Ensure a clean slate for the test
    if os.path.exists(metrics_file):
        os.remove(metrics_file)

    # We must run this as the 'user' if the pytest is running as root, but typically the test runs in the correct context.
    # Assuming the test suite runs as the appropriate user or root with access to the user's systemd.
    # We will use the systemctl --user command as specified.

    # Ensure systemd user instance is active
    os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000" # Common for user 1000, fallback if needed

    start_time = time.time()

    try:
        subprocess.run(["su", "-", "user", "-c", "systemctl --user restart fast-exporter.service"], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["systemctl", "--user", "restart", "fast-exporter.service"], check=True)
        except subprocess.CalledProcessError:
            pytest.fail("Failed to restart systemd user service 'fast-exporter.service'")

    # Poll for output
    while not os.path.exists(metrics_file):
        time.sleep(0.1)
        if time.time() - start_time > 15.0:
            pytest.fail("Timeout: Service took too long or failed to produce metrics.json")

    end_time = time.time()
    runtime = end_time - start_time

    # Validate metric correctness
    with open(metrics_file) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not valid JSON")

    assert data.get("timezone_parsed") is True, "Timezone parsing failed. Locale/TZ not set properly in service environment."

    assert runtime <= 3.0, f"Performance threshold not met: runtime was {runtime:.2f}s, expected <= 3.0s (Cython compilation likely failed)"