# test_final_state.py

import os
import subprocess
import time
import shutil
import pytest

def test_filter_executable():
    """Verify that the filter binary exists and is an ELF executable."""
    filter_path = "/home/user/filter"
    assert os.path.exists(filter_path), f"Filter binary not found at {filter_path}"
    assert os.path.isfile(filter_path), f"{filter_path} is not a file"
    assert os.access(filter_path, os.X_OK), f"{filter_path} is not executable"

    with open(filter_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{filter_path} is not an ELF executable"

def test_systemd_service_active():
    """Verify that the mailer-daemon systemd user service is active."""
    service_name = "mailer-daemon.service"

    # Setup environment to run systemctl --user correctly if running as root during test
    env = os.environ.copy()
    if "XDG_RUNTIME_DIR" not in env:
        # Assuming user ID 1000 for 'user'
        env["XDG_RUNTIME_DIR"] = "/run/user/1000"

    # Run as 'user' using su if we are root, or just systemctl if we are 'user'
    cmd = ["su", "-", "user", "-c", f"XDG_RUNTIME_DIR=/run/user/1000 systemctl --user is-active {service_name}"]
    if os.geteuid() != 0:
        cmd = ["systemctl", "--user", "is-active", service_name]

    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True
        )
        assert result.stdout.strip() == "active", f"Service {service_name} is not active. Output: {result.stdout.strip()}"
    except Exception as e:
        pytest.fail(f"Failed to check systemd service: {e}")

def test_adversarial_corpus():
    """Verify the filter correctly classifies the clean and evil corpora."""
    filter_path = "/home/user/filter"
    clean_dir = "/app/evaluation_corpus/clean"
    evil_dir = "/app/evaluation_corpus/evil"

    assert os.path.exists(clean_dir), f"Clean corpus directory not found at {clean_dir}"
    assert os.path.exists(evil_dir), f"Evil corpus directory not found at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No files found in clean evaluation corpus"
    assert len(evil_files) > 0, "No files found in evil evaluation corpus"

    clean_failed = []
    for cf in clean_files:
        # Run filter on clean file, expect exit code 0
        res = subprocess.run([filter_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        # Run filter on evil file, expect exit code 1
        res = subprocess.run([filter_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_daemon_processing():
    """Verify the daemon processes incoming files correctly."""
    incoming_dir = "/home/user/spool/incoming"
    processed_dir = "/home/user/spool/processed"
    quarantine_dir = "/home/user/spool/quarantine"

    assert os.path.isdir(incoming_dir), f"Directory {incoming_dir} does not exist"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist"
    assert os.path.isdir(quarantine_dir), f"Directory {quarantine_dir} does not exist"

    clean_files = os.listdir("/app/evaluation_corpus/clean")
    evil_files = os.listdir("/app/evaluation_corpus/evil")

    if not clean_files or not evil_files:
        pytest.skip("Evaluation corpus is empty, cannot test daemon processing")

    clean_sample = os.path.join("/app/evaluation_corpus/clean", clean_files[0])
    evil_sample = os.path.join("/app/evaluation_corpus/evil", evil_files[0])

    test_clean = os.path.join(incoming_dir, "test_clean.eml")
    test_evil = os.path.join(incoming_dir, "test_evil.eml")

    # Cleanup before test if needed
    for path in [test_clean, test_evil, os.path.join(processed_dir, "test_clean.eml"), os.path.join(quarantine_dir, "test_evil.eml")]:
        if os.path.exists(path):
            os.remove(path)

    # Drop files into incoming
    shutil.copy(clean_sample, test_clean)
    shutil.copy(evil_sample, test_evil)

    # Ensure they have proper ownership if running as root
    if os.geteuid() == 0:
        os.chown(test_clean, 1000, 1000)
        os.chown(test_evil, 1000, 1000)

    # Wait for daemon to process
    time.sleep(3)

    if os.path.exists(test_clean):
        pytest.fail("Clean file remained in incoming/ and was not processed")
    if os.path.exists(test_evil):
        pytest.fail("Evil file remained in incoming/ and was not processed")

    assert os.path.exists(os.path.join(processed_dir, "test_clean.eml")), "Clean email did not move to processed/"
    assert os.path.exists(os.path.join(quarantine_dir, "test_evil.eml")), "Evil email did not move to quarantine/"