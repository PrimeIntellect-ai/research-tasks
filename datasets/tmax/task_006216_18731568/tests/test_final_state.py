# test_final_state.py

import os
import subprocess
import time
import re
import signal

KEEPALIVE_SCRIPT = "/home/user/keepalive.py"
WORKER_SCRIPT = "/home/user/worker.py"
PID_FILE = "/home/user/worker.pid"
LOG_FILE = "/home/user/monitor.log"

def cleanup():
    """Kill any running worker processes and remove state files."""
    try:
        subprocess.run(["pkill", "-f", "worker.py"], check=False)
    except Exception:
        pass
    for f in [PID_FILE, LOG_FILE]:
        if os.path.exists(f):
            os.remove(f)

def is_process_running(pid):
    """Check if a process with the given PID is running."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def test_keepalive_script():
    """Test the complete behavior of the keepalive script."""
    # 1. Verify script exists and is executable
    assert os.path.exists(KEEPALIVE_SCRIPT), f"{KEEPALIVE_SCRIPT} does not exist."
    assert os.access(KEEPALIVE_SCRIPT, os.X_OK), f"{KEEPALIVE_SCRIPT} is not executable."

    # Setup clean state
    cleanup()

    try:
        # 2. Run keepalive.py when no worker is running
        result = subprocess.run([KEEPALIVE_SCRIPT], capture_output=True, text=True)
        assert result.returncode == 0, f"{KEEPALIVE_SCRIPT} failed with return code {result.returncode}. Stderr: {result.stderr}"

        # 3. Check PID file
        assert os.path.exists(PID_FILE), f"{PID_FILE} was not created."
        with open(PID_FILE, "r") as f:
            pid_str = f.read().strip()
        assert pid_str.isdigit(), f"{PID_FILE} does not contain a valid integer PID."
        pid1 = int(pid_str)

        # 4. Check process is running
        assert is_process_running(pid1), f"Process {pid1} is not running."

        # Give it a moment to ensure background execution
        time.sleep(0.5)

        # 5. Check log file
        assert os.path.exists(LOG_FILE), f"{LOG_FILE} was not created."
        with open(LOG_FILE, "r") as f:
            log_lines = f.read().strip().split('\n')
        assert len(log_lines) == 1, f"Expected 1 log line, found {len(log_lines)}."
        log_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] RESTARTED$")
        assert log_pattern.match(log_lines[0]), f"Log line format incorrect: {log_lines[0]}"

        # 6. Run keepalive.py again (should do nothing)
        result = subprocess.run([KEEPALIVE_SCRIPT], capture_output=True, text=True)
        assert result.returncode == 0, f"{KEEPALIVE_SCRIPT} failed on second run."

        # 7. Verify PID hasn't changed
        with open(PID_FILE, "r") as f:
            pid_str2 = f.read().strip()
        assert int(pid_str2) == pid1, "PID changed when worker was already running."

        # 8. Verify log hasn't changed
        with open(LOG_FILE, "r") as f:
            log_lines2 = f.read().strip().split('\n')
        assert len(log_lines2) == 1, "Log file was appended to when worker was already running."

        # 9. Kill the worker
        os.kill(pid1, signal.SIGKILL)
        time.sleep(0.5)
        assert not is_process_running(pid1), "Failed to kill worker process."

        # 10. Run keepalive.py again
        result = subprocess.run([KEEPALIVE_SCRIPT], capture_output=True, text=True)
        assert result.returncode == 0, f"{KEEPALIVE_SCRIPT} failed on third run."

        # 11. Verify new PID
        with open(PID_FILE, "r") as f:
            pid_str3 = f.read().strip()
        assert pid_str3.isdigit(), f"{PID_FILE} does not contain a valid integer PID."
        pid3 = int(pid_str3)
        assert pid3 != pid1, "PID did not change after worker was killed and restarted."

        # 12. Verify new process is running
        assert is_process_running(pid3), f"New process {pid3} is not running."

        # 13. Verify log has two lines
        with open(LOG_FILE, "r") as f:
            log_lines3 = f.read().strip().split('\n')
        assert len(log_lines3) == 2, f"Expected 2 log lines, found {len(log_lines3)}."
        assert log_pattern.match(log_lines3[1]), f"Second log line format incorrect: {log_lines3[1]}"

    finally:
        cleanup()