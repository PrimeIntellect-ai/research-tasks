# test_final_state.py
import os
import tarfile
import re
import subprocess
import glob
import pytest

def test_backup_archive():
    """Test that the legacy backup archive exists, is valid tar.gz, and contains the config file."""
    backup_path = "/home/user/legacy_backup.tar.gz"
    assert os.path.exists(backup_path), f"Backup archive {backup_path} does not exist."
    assert tarfile.is_tarfile(backup_path), f"File {backup_path} is not a valid tar archive."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if legacy_monitor/config.json is in the archive
            found = any("legacy_monitor/config.json" in name for name in names)
            assert found, f"Archive does not contain 'legacy_monitor/config.json'. Contents: {names}"
    except tarfile.ReadError:
        pytest.fail(f"Could not read {backup_path} as a gzip-compressed tar archive.")

def test_tunnel_script():
    """Test that the tunnel script exists, is executable, and contains the correct SSH command."""
    script_path = "/home/user/tunnel.sh"
    assert os.path.exists(script_path), f"Tunnel script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Tunnel script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    pattern = r"ssh.*-L.*9999:remote-telemetry\.internal:80.*deploy@bastion\.internal"
    assert re.search(pattern, content), f"Tunnel script does not contain the correct ssh command. Content: {content}"

def test_dropped_frames():
    """Test that the dropped frames count is correctly calculated and saved."""
    frames_path = "/home/user/dropped_frames.txt"
    assert os.path.exists(frames_path), f"Dropped frames file {frames_path} does not exist."

    with open(frames_path, "r") as f:
        content = f.read().strip()

    assert content == "14", f"Expected dropped frames count to be '14', but got '{content}'."

def test_sanitizer_adversarial_corpus():
    """Test the sanitizer script against the clean and evil corpora."""
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.exists(sanitizer_path), f"Sanitizer script {sanitizer_path} does not exist."

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    # We allow the files to be any file in the directory, assuming they are json or txt logs
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run(["python3", sanitizer_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run(["python3", sanitizer_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))