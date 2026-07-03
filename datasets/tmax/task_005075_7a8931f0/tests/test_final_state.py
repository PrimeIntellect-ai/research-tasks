# test_final_state.py

import os
import re
import subprocess
import tempfile
import zipfile
import pytest

def test_sshd_config_hardened():
    """Verify the sshd_config_hardened file exists and contains correct settings."""
    config_path = "/home/user/sshd_config_hardened"
    assert os.path.isfile(config_path), f"Missing sshd_config_hardened file at {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Case-insensitive checks for Port 22022 and PermitRootLogin no
    assert re.search(r"(?i)^\s*Port\s+22022\b", content, re.MULTILINE), "sshd_config_hardened is missing 'Port 22022'"
    assert re.search(r"(?i)^\s*PermitRootLogin\s+no\b", content, re.MULTILINE), "sshd_config_hardened is missing 'PermitRootLogin no'"

def test_detector_executable():
    """Verify the detector script exists and is executable."""
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Missing detector script at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector script at {detector_path} is not executable"

def test_adversarial_corpus():
    """Verify the detector correctly classifies the evil and clean corpora."""
    detector_path = "/home/user/detector"
    zip_path = "/app/evidence.zip"
    password = b"alphatango7"

    assert os.path.isfile(zip_path), f"Missing evidence.zip at {zip_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(path=tmpdir, pwd=password)
        except Exception as e:
            pytest.fail(f"Failed to extract {zip_path} with password {password.decode()}: {e}")

        evil_dir = os.path.join(tmpdir, "evil")
        clean_dir = os.path.join(tmpdir, "clean")

        assert os.path.isdir(evil_dir), "Extracted zip is missing 'evil' directory"
        assert os.path.isdir(clean_dir), "Extracted zip is missing 'clean' directory"

        evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
        clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

        evil_bypassed = []
        for filename in evil_files:
            filepath = os.path.join(evil_dir, filename)
            with open(filepath, "rb") as f:
                payload = f.read()

            result = subprocess.run([detector_path], input=payload, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                evil_bypassed.append(filename)

        clean_modified = []
        for filename in clean_files:
            filepath = os.path.join(clean_dir, filename)
            with open(filepath, "rb") as f:
                payload = f.read()

            result = subprocess.run([detector_path], input=payload, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                clean_modified.append(filename)

        error_msgs = []
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

        if error_msgs:
            pytest.fail("; ".join(error_msgs))