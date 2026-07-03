# test_final_state.py
import os
import subprocess
import time
import re

def test_files_exist():
    """Verify all required files exist."""
    required_files = [
        "/home/user/micro_mailer",
        "/home/user/auto_dispatch.exp",
        "/home/user/.config/systemd/user/mailer_daemon.service",
        "/home/user/.config/systemd/user/dispatch_job.service"
    ]
    for f in required_files:
        assert os.path.isfile(f), f"Required file {f} is missing."

    # Check if micro_mailer is executable
    assert os.access("/home/user/micro_mailer", os.X_OK), "/home/user/micro_mailer is not executable."

def test_systemd_mailer_daemon():
    """Verify mailer_daemon.service configuration."""
    with open("/home/user/.config/systemd/user/mailer_daemon.service", "r") as f:
        content = f.read()

    assert re.search(r"Restart\s*=\s*always", content), "mailer_daemon.service must have Restart=always."
    assert "/home/user/micro_mailer" in content, "mailer_daemon.service must execute /home/user/micro_mailer."

def test_systemd_dispatch_job():
    """Verify dispatch_job.service configuration."""
    with open("/home/user/.config/systemd/user/dispatch_job.service", "r") as f:
        content = f.read()

    assert re.search(r"Type\s*=\s*oneshot", content), "dispatch_job.service must have Type=oneshot."
    assert re.search(r"After\s*=\s*.*mailer_daemon\.service", content), "dispatch_job.service must run After mailer_daemon.service."
    assert re.search(r"(Requires|BindsTo)\s*=\s*.*mailer_daemon\.service", content), "dispatch_job.service must Require mailer_daemon.service."
    assert "/home/user/auto_dispatch.exp" in content, "dispatch_job.service must execute the expect script."

def test_daemon_and_expect_interaction():
    """Verify the daemon and expect script work together to write the log."""
    log_file = "/home/user/digest.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    daemon_process = subprocess.Popen(["/home/user/micro_mailer"])
    try:
        # Wait for daemon to bind to port
        time.sleep(1.0)

        # Run expect script
        result = subprocess.run(["/usr/bin/expect", "/home/user/auto_dispatch.exp"], capture_output=True, text=True)
        assert result.returncode == 0, f"Expect script failed with output: {result.stderr}"

        # Wait for file write
        time.sleep(0.5)

        assert os.path.isfile(log_file), "/home/user/digest.log was not created."
        with open(log_file, "r") as f:
            log_content = f.read()

        assert "DIGEST_DISPATCHED_TO_LIST" in log_content, "Log file does not contain the expected string."
    finally:
        daemon_process.terminate()
        daemon_process.wait(timeout=2)