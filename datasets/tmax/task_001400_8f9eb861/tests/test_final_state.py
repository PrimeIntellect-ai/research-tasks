# test_final_state.py
import os
import time
import subprocess
import signal

def test_symlink_created_correctly():
    symlink_path = "/home/user/dash_app/current_metrics"
    target_path = "/home/user/metrics_data"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.readlink(symlink_path) == target_path, f"{symlink_path} does not point to {target_path}."

def test_supervisor_script_executable():
    script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_supervisor_script_behavior():
    script_path = "/home/user/supervisor.sh"
    log_path = "/home/user/dash_app/supervision.log"

    # Ensure a clean slate
    if os.path.exists(log_path):
        os.remove(log_path)

    # Start the supervisor script
    process = subprocess.Popen(
        [script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )

    try:
        # Let it run for 6 seconds to trigger at least one crash
        time.sleep(6)
    finally:
        # Clean up the supervisor and any child processes
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

        # Also clean up any lingering dashboard processes just in case
        subprocess.run(["pkill", "-f", "python3 /home/user/dash_app/dashboard.py"], capture_output=True)

    assert os.path.isfile(log_path), f"Log file {log_path} was not created by the supervisor."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "RESTART_EVENT | TOTAL_CRASHES: 1" in log_content, (
        f"Expected 'RESTART_EVENT | TOTAL_CRASHES: 1' in log, but got:\n{log_content}"
    )