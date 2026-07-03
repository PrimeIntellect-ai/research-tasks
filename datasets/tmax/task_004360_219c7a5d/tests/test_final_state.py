# test_final_state.py

import os
import subprocess
import time
import socket
import ssl
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_deploy_script():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} is missing"
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable"

    # Run the deployment script in the background
    proc = subprocess.Popen(["bash", deploy_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Allow some time for background services (SMTP, HTTPS, bindfs) to start
    time.sleep(3)

    yield

    # Cleanup after tests
    proc.terminate()
    subprocess.run(["pkill", "-f", "smtpd"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "8443"], stderr=subprocess.DEVNULL)
    subprocess.run(["umount", "/home/user/live_logs"], stderr=subprocess.DEVNULL)

def test_bindfs_mount():
    with open("/proc/mounts", "r") as f:
        mounts = f.read()

    assert "/home/user/live_logs" in mounts, "/home/user/live_logs is not mounted"

    # Verify it is mounted read-only
    try:
        test_file = "/home/user/live_logs/test_ro_write"
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        pytest.fail("/home/user/live_logs is not mounted read-only")
    except OSError:
        pass # Expected behavior for read-only filesystem

def test_smtp_server_running():
    try:
        with socket.create_connection(("localhost", 1025), timeout=2) as s:
            pass
    except Exception as e:
        pytest.fail(f"Could not connect to SMTP server on port 1025: {e}")

def test_https_dashboard_running():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection(("localhost", 8443), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname="localhost") as ssock:
                pass
    except Exception as e:
        pytest.fail(f"Could not connect to HTTPS dashboard on port 8443 with TLS: {e}")

def test_detector_adversarial_corpus():
    detector_bin = "/home/user/bin/detector"
    assert os.path.isfile(detector_bin), f"Detector binary not found at {detector_bin}"
    assert os.access(detector_bin, os.X_OK), f"Detector binary is not executable"

    evil_dir = "/home/user/corpora/evil"
    clean_dir = "/home/user/corpora/clean"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        proc = subprocess.run([detector_bin, path], capture_output=True, text=True)
        lines = [line for line in proc.stdout.strip().split("\n") if line]
        for line in lines:
            if not line.startswith("[ALERT]"):
                evil_bypassed.append(f)
                break

    # Test clean corpus
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        proc = subprocess.run([detector_bin, path], capture_output=True, text=True)
        lines = [line for line in proc.stdout.strip().split("\n") if line]
        for line in lines:
            if not line.startswith("[OK]"):
                clean_modified.append(f)
                break

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_alert_mailer_fixed():
    mailer_dir = "/app/alert-mailer-1.0.0"

    # Build the package
    build_proc = subprocess.run(["cargo", "build", "--release"], cwd=mailer_dir, capture_output=True, text=True)
    assert build_proc.returncode == 0, f"Failed to build alert-mailer:\n{build_proc.stderr}"

    mailer_bin = os.path.join(mailer_dir, "target/release/alert-mailer")
    assert os.path.isfile(mailer_bin), "alert-mailer binary not found after build"

    # Test connection logic
    test_proc = subprocess.run([mailer_bin, "--test"], cwd=mailer_dir, capture_output=True, text=True)
    assert test_proc.returncode == 0, f"alert-mailer failed to run or connect to port 1025:\n{test_proc.stderr}\n{test_proc.stdout}"