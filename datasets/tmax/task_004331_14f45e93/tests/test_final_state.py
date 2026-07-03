# test_final_state.py
import os
import stat
import subprocess
import time
import re

def test_monitor_executable_exists():
    assert os.path.isfile("/home/user/monitor.cpp"), "/home/user/monitor.cpp does not exist."
    assert os.path.isfile("/home/user/monitor"), "/home/user/monitor does not exist."
    assert os.access("/home/user/monitor", os.X_OK), "/home/user/monitor is not executable."

def test_monitor_functionality_running_process():
    log_file = "/home/user/logs/process_status.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    # Start a background process
    proc = subprocess.Popen(["sleep", "10"])
    time.sleep(0.5)

    try:
        # Run monitor
        subprocess.run(["/home/user/monitor", "sleep"], check=True)

        assert os.path.exists(log_file), "Log file was not created."
        with open(log_file, "r") as f:
            lines = f.readlines()

        assert len(lines) >= 1, "Log file is empty."
        last_line = lines[-1].strip()

        # We don't know the exact PID if there are multiple sleeps, but it should match the pattern
        assert re.match(r"^STATUS: sleep IS RUNNING \(PID: \d+\)$", last_line), f"Log line format incorrect: {last_line}"

        # Check permissions
        st = os.stat(log_file)
        perms = stat.S_IMODE(st.st_mode)
        assert perms == 0o600, f"Permissions of {log_file} should be 600, but are {oct(perms)}."
    finally:
        proc.terminate()
        proc.wait()

def test_monitor_functionality_not_running_process():
    log_file = "/home/user/logs/process_status.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    subprocess.run(["/home/user/monitor", "definitely_not_running_proc"], check=True)

    assert os.path.exists(log_file), "Log file was not created."
    with open(log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 1, "Log file is empty."
    last_line = lines[-1].strip()

    expected = "STATUS: definitely_not_running_proc IS NOT RUNNING"
    assert last_line == expected, f"Expected '{expected}', got '{last_line}'"

def test_monitor_log_rotation():
    log_file = "/home/user/logs/process_status.log"
    backup_file = "/home/user/logs/process_status.log.1"

    # Ensure a clean state for rotation test
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(backup_file):
        os.remove(backup_file)

    # Write 5 lines
    for _ in range(5):
        subprocess.run(["/home/user/monitor", "definitely_not_running_proc"], check=True)

    assert not os.path.exists(backup_file), "Backup file created prematurely."

    # 6th run should trigger rotation
    subprocess.run(["/home/user/monitor", "definitely_not_running_proc"], check=True)

    assert os.path.exists(backup_file), "Log rotation did not occur; backup file missing."

def test_cron_configuration():
    cron_file = "/home/user/monitor_cron"
    assert os.path.isfile(cron_file), f"{cron_file} does not exist."

    with open(cron_file, "r") as f:
        content = f.read().strip()

    pattern = r"^\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/monitor\s+qemu-system-x86_64$"
    assert re.search(pattern, content, re.MULTILINE), "Cron configuration is incorrect."

def test_fstab_configuration():
    fstab_file = "/home/user/sandbox_fstab"
    assert os.path.isfile(fstab_file), f"{fstab_file} does not exist."

    with open(fstab_file, "r") as f:
        content = f.read().strip()

    pattern = r"^/home/user/data\s+/sandbox/data\s+none\s+bind,ro,nosuid,nodev\s+0\s+0$"
    assert re.search(pattern, content, re.MULTILINE), "fstab configuration is incorrect."