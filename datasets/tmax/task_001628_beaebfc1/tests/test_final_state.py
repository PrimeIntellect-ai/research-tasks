# test_final_state.py

import os
import subprocess
import re

SCRIPT_PATH = "/home/user/monitor/integrity_monitor.sh"
BASELINE_PATH = "/home/user/monitor/baseline.md5"
ALERTS_PATH = "/home/user/monitor/alerts.log"
PROTECTED_DIR = "/home/user/protected_data"

def test_script_exists_and_executable():
    """Verify that the script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_functionality():
    """Verify baseline creation, modification detection, and log rotation."""
    # Ensure clean state for testing functionality
    if os.path.exists(BASELINE_PATH):
        os.remove(BASELINE_PATH)
    if os.path.exists(ALERTS_PATH):
        os.remove(ALERTS_PATH)
    for ext in [".1", ".2", ".3"]:
        if os.path.exists(ALERTS_PATH + ext):
            os.remove(ALERTS_PATH + ext)

    # First run (Baseline Creation)
    subprocess.run([SCRIPT_PATH], check=True)
    assert os.path.isfile(BASELINE_PATH), "Baseline file was not created on first run."
    if os.path.exists(ALERTS_PATH):
        with open(ALERTS_PATH, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 0, "Alerts log should be empty or not created on first run."

    # Second run (Modification Detection)
    file1 = os.path.join(PROTECTED_DIR, "file1.txt")
    with open(file1, "w") as f:
        f.write("changed\n")

    subprocess.run([SCRIPT_PATH], check=True)
    assert os.path.isfile(ALERTS_PATH), "Alerts log was not created after modification."

    with open(ALERTS_PATH, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 1, "Alerts log is empty after modification."
        last_line = lines[-1].strip()
        regex = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ALERT: \/home\/user\/protected_data\/file1\.txt modified or created$"
        assert re.match(regex, last_line), f"Alert line format incorrect: {last_line}"

    # Third run (Log Rotation Test)
    with open(ALERTS_PATH, "a") as f:
        for i in range(1, 6):
            f.write(f"Dummy log line {i}\n")

    file3 = os.path.join(PROTECTED_DIR, "file3.txt")
    with open(file3, "w") as f:
        f.write("new file\n")

    subprocess.run([SCRIPT_PATH], check=True)

    assert os.path.isfile(ALERTS_PATH + ".1"), "Log rotation failed: alerts.log.1 not created."

    with open(ALERTS_PATH, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 1, f"Expected exactly 1 line in new alerts.log after rotation, got {len(lines)}"
        last_line = lines[0].strip()
        regex = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ALERT: \/home\/user\/protected_data\/file3\.txt modified or created$"
        assert re.match(regex, last_line), f"Alert line format incorrect after rotation: {last_line}"

def test_cron_job():
    """Verify that the cron job is correctly scheduled."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    # If crontab is empty or doesn't exist for user, returncode might be 1, but we should check output.
    output = result.stdout
    regex = r"\*/5\s+\*\s+\*\s+\*\s+\*\s+.*\/home\/user\/monitor\/integrity_monitor.sh"
    assert re.search(regex, output), "Cron job not found or incorrect format in crontab."