# test_final_state.py

import os
import subprocess
import time
import pytest

def test_tenant_deduplication():
    baseline = "/home/user/tenants/baseline/config.json"
    assert os.path.isfile(baseline), f"Missing baseline config at {baseline}"

    baseline_inode = os.stat(baseline).st_ino

    identical_tenants = [
        "/home/user/tenants/tenant_1/config.json",
        "/home/user/tenants/tenant_3/config.json",
        "/home/user/tenants/tenant_4/config.json"
    ]

    different_tenants = [
        "/home/user/tenants/tenant_2/config.json",
        "/home/user/tenants/tenant_5/config.json"
    ]

    for t in identical_tenants:
        assert os.path.isfile(t), f"Missing config file at {t}"
        assert os.stat(t).st_ino == baseline_inode, f"File {t} is not hardlinked to the baseline config. Deduplication failed."

    for t in different_tenants:
        assert os.path.isfile(t), f"Missing config file at {t}"
        assert os.stat(t).st_ino != baseline_inode, f"File {t} was incorrectly hardlinked to the baseline config, but it had different content."

def test_rotate_script_exists_and_works():
    rotate_script = "/home/user/rotate.sh"
    assert os.path.isfile(rotate_script), f"Missing rotate script at {rotate_script}"
    assert os.access(rotate_script, os.X_OK), f"Script {rotate_script} is not executable"

    # Execute the rotate script to verify behavior
    try:
        subprocess.run([rotate_script], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {rotate_script} failed with error: {e.stderr.decode()}")

    # Give the service a moment to handle the signal
    time.sleep(1)

    rotated_log = "/home/user/logs/billing.log.1"
    assert os.path.isfile(rotated_log), f"Log rotation failed: {rotated_log} was not created."

    current_log = "/home/user/logs/billing.log"
    assert os.path.isfile(current_log), f"Current log file {current_log} is missing after rotation."

    with open(current_log, "r") as f:
        content = f.read()

    assert "Log reopened" in content, "The billing process did not reopen its log. SIGUSR1 may not have been sent correctly."

def test_monitor_c_compiled():
    monitor_c = "/home/user/monitor.c"
    monitor_bin = "/home/user/monitor"

    assert os.path.isfile(monitor_c), f"Source file {monitor_c} is missing."
    assert os.path.isfile(monitor_bin), f"Compiled binary {monitor_bin} is missing."
    assert os.access(monitor_bin, os.X_OK), f"Compiled binary {monitor_bin} is not executable."