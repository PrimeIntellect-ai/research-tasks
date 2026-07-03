# test_final_state.py

import os
import re
import time
import signal
import subprocess
import pytest

def test_fstab_fixed():
    fstab_path = "/home/user/system/fstab.iot"
    assert os.path.isfile(fstab_path), f"fstab file {fstab_path} is missing."

    with open(fstab_path, "r") as f:
        content = f.read()

    # Check for the correctly formatted bind mount line
    pattern = r"^/home/user/iot_storage\s+/mnt/iot_data\s+bind\s+defaults,bind\s+0\s+0$"
    match = any(re.match(pattern, line.strip()) for line in content.splitlines())
    assert match, "fstab.iot does not contain the correct bind mount configuration for /home/user/iot_storage."

def test_mail_conf_fixed():
    mail_conf_path = "/home/user/config/mail.conf"
    assert os.path.isfile(mail_conf_path), f"mail.conf file {mail_conf_path} is missing."

    with open(mail_conf_path, "r") as f:
        content = f.read()

    assert re.search(r"^SMTP_HOST=127\.0\.0\.1$", content, re.MULTILINE), "SMTP_HOST is not set to 127.0.0.1 in mail.conf."
    assert re.search(r"^SMTP_PORT=2525$", content, re.MULTILINE), "SMTP_PORT is not set to 2525 in mail.conf."

def test_script_permissions_and_content():
    script_path = "/home/user/start_iot.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert content.startswith("#!/bin/bash"), "Script does not start with #!/bin/bash."
    assert re.search(r"set\s+-[^\n]*e", content) or "set -e" in content, "Script does not contain 'set -e'."
    assert re.search(r"set\s+-[^\n]*u", content) or "set -u" in content, "Script does not contain 'set -u'."
    assert "wait" in content, "Script does not use 'wait' to block for background processes."

def test_script_execution_and_trap():
    script_path = "/home/user/start_iot.sh"

    # Start the script as a subprocess
    proc = subprocess.Popen(
        [script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Give the script time to start background processes
    time.sleep(1.5)

    # Verify that the background processes are running
    smtp_running = subprocess.run(["pgrep", "-f", "smtp_edge.py"], capture_output=True).returncode == 0
    sensor_running = subprocess.run(["pgrep", "-f", "sensor_app.sh"], capture_output=True).returncode == 0

    if not smtp_running or not sensor_running:
        proc.kill()
        pytest.fail("The script did not successfully start both smtp_edge.py and sensor_app.sh in the background.")

    # Send SIGTERM to the script to trigger the trap
    os.kill(proc.pid, signal.SIGTERM)

    try:
        stdout, stderr = proc.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        pytest.fail("The script did not exit gracefully after receiving SIGTERM (trap failed or wait hung).")

    # Check that CLEANUP_SUCCESS was printed
    assert "CLEANUP_SUCCESS" in stdout, "The script did not print 'CLEANUP_SUCCESS' upon termination."

    # Verify that the child processes were killed by the trap
    smtp_dead = subprocess.run(["pgrep", "-f", "smtp_edge.py"], capture_output=True).returncode != 0
    sensor_dead = subprocess.run(["pgrep", "-f", "sensor_app.sh"], capture_output=True).returncode != 0

    assert smtp_dead, "smtp_edge.py was not killed by the script's cleanup trap."
    assert sensor_dead, "sensor_app.sh was not killed by the script's cleanup trap."