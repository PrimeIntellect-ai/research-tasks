# test_final_state.py

import os
import subprocess
import re
import stat

def test_scripts_exist_and_executable():
    """Verify that the required scripts exist and are executable."""
    poll_script = "/home/user/poll_vm.py"
    deploy_script = "/home/user/deploy_job.sh"

    assert os.path.isfile(poll_script), f"FAIL: {poll_script} does not exist."
    assert os.access(poll_script, os.X_OK), f"FAIL: {poll_script} is not executable."

    assert os.path.isfile(deploy_script), f"FAIL: {deploy_script} does not exist."
    assert os.access(deploy_script, os.X_OK), f"FAIL: {deploy_script} is not executable."

def test_deploy_job_idempotency_and_cron():
    """Run deploy_job.sh again and verify cron job is installed exactly once."""
    deploy_script = "/home/user/deploy_job.sh"

    # Run the deploy script again to test idempotency
    try:
        subprocess.run(["/bin/bash", deploy_script], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"FAIL: Running {deploy_script} failed with error: {e.stderr.decode()}")

    # Check crontab
    try:
        crontab_out = subprocess.check_output(["crontab", "-l"]).decode()
    except subprocess.CalledProcessError:
        crontab_out = ""

    # Count occurrences of poll_vm.py
    count = crontab_out.count("/home/user/poll_vm.py")
    assert count == 1, f"FAIL: Expected exactly 1 cron job for poll_vm.py, found {count}."

    # Check that it runs every minute
    cron_lines = [line for line in crontab_out.splitlines() if "/home/user/poll_vm.py" in line]
    assert len(cron_lines) == 1
    assert cron_lines[0].strip().startswith("* * * * *"), "FAIL: Cron job is not scheduled to run every minute (* * * * *)."

def test_csv_content_and_format():
    """Verify the CSV file header and data rows."""
    csv_file = "/home/user/vm_capacity.csv"
    assert os.path.isfile(csv_file), f"FAIL: {csv_file} does not exist."

    with open(csv_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"FAIL: {csv_file} must contain a header and at least one data row."

    # Verify header
    assert lines[0] == "TIMESTAMP,VNC_STATUS,PID,RSS_KB", "FAIL: Incorrect or missing CSV header."

    # Verify header is not duplicated
    header_count = lines.count("TIMESTAMP,VNC_STATUS,PID,RSS_KB")
    assert header_count == 1, "FAIL: CSV header is duplicated, script is not idempotent."

    # Verify the last data row
    tail_line = lines[-1]

    # Regex check: [YYYY-MM-DD HH:MM:SS],UP/DOWN,<digits>,<digits>
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\],(UP|DOWN),\d+,\d+$"
    assert re.match(pattern, tail_line), f"FAIL: Data row incorrectly formatted. Found: {tail_line}"

    # Verify PID matches actual QEMU PID
    try:
        actual_pid = subprocess.check_output(["pgrep", "qemu-system-x86"]).decode().strip()
    except subprocess.CalledProcessError:
        actual_pid = ""

    assert actual_pid, "FAIL: qemu-system-x86 is not running."

    logged_pid = tail_line.split(',')[2]
    assert actual_pid == logged_pid, f"FAIL: Logged PID ({logged_pid}) does not match actual running QEMU PID ({actual_pid})."