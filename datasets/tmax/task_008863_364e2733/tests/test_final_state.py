# test_final_state.py
import os
import stat
import time
import subprocess
import signal

def test_directory_structure():
    """Verify that the required directory structure exists."""
    expected_dirs = [
        "/home/user/watchdog",
        "/home/user/watchdog/links",
        "/home/user/watchdog/logs",
        "/home/user/watchdog/targets"
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Directory {d} is missing."

def test_daemon_script_executable():
    """Verify that daemon.sh exists and is executable."""
    script_path = "/home/user/watchdog/daemon.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_daemon_behavior():
    """Test the watchdog daemon's start, logging, rotation, and stop behavior."""
    script_path = "/home/user/watchdog/daemon.sh"
    pid_file = "/home/user/watchdog/daemon.pid"
    links_dir = "/home/user/watchdog/links"
    targets_dir = "/home/user/watchdog/targets"
    log_file = "/home/user/watchdog/logs/watch.log"
    old_log_file = "/home/user/watchdog/logs/watch.log.old"

    # Clean up any previous state
    subprocess.run([script_path, "stop"], capture_output=True)
    for f in [pid_file, log_file, old_log_file]:
        if os.path.exists(f):
            os.remove(f)
    for f in os.listdir(links_dir):
        os.remove(os.path.join(links_dir, f))
    for f in os.listdir(targets_dir):
        os.remove(os.path.join(targets_dir, f))

    # Start the daemon
    result = subprocess.run([script_path, "start"], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to start daemon: {result.stderr}"

    # Wait a bit for the daemon to initialize
    time.sleep(1)

    # Check PID file
    assert os.path.isfile(pid_file), "PID file was not created."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), "PID file does not contain a valid numeric PID."
    pid = int(pid_str)

    # Verify process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, "The process specified in the PID file is not running."

    # Create test files and links
    # 1. Broken link
    broken_link = os.path.join(links_dir, "broken_link")
    os.symlink(os.path.join(targets_dir, "nonexistent"), broken_link)

    # 2. Bad permission link
    bad_target = os.path.join(targets_dir, "target1")
    with open(bad_target, "w") as f:
        f.write("bad")
    os.chmod(bad_target, 0o644)
    bad_link = os.path.join(links_dir, "bad_link")
    os.symlink(bad_target, bad_link)

    # 3. Good permission link
    good_target = os.path.join(targets_dir, "target2")
    with open(good_target, "w") as f:
        f.write("good")
    os.chmod(good_target, 0o600)
    good_link = os.path.join(links_dir, "good_link")
    os.symlink(good_target, good_link)

    # Wait for logs to be written and rotation to occur
    # Each iteration should write approx 35-40 bytes. 3 iterations > 100 bytes.
    time.sleep(5)

    # Stop the daemon
    subprocess.run([script_path, "stop"], capture_output=True)

    # Verify stop behavior
    assert not os.path.exists(pid_file), "PID file was not removed after stop."
    try:
        os.kill(pid, 0)
        process_running = True
    except OSError:
        process_running = False
    assert not process_running, "The background process was not terminated after stop."

    # Verify logs
    log_contents = ""
    if os.path.exists(old_log_file):
        with open(old_log_file, "r") as f:
            log_contents += f.read()
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_contents += f.read()

    assert "BROKEN: broken_link" in log_contents, "Missing expected log entry for broken link."
    assert "BADPERM: bad_link 644" in log_contents, "Missing expected log entry for bad permissions."
    assert "good_link" not in log_contents, "Log should not contain entries for valid links."

    # Verify rotation occurred
    assert os.path.exists(old_log_file), "Log rotation did not occur (watch.log.old is missing)."