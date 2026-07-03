# test_final_state.py

import os
import re
import subprocess
import urllib.request
import ssl
import pytest

def test_mount_and_fstab():
    """Verify that the image is mounted and fstab is updated."""
    mount_point = "/mnt/evidence"
    assert os.path.ismount(mount_point), f"{mount_point} is not a mount point."

    with open("/etc/fstab", "r") as f:
        fstab_content = f.read()

    fstab_regex = re.compile(r"^/app/evidence\.img\s+/mnt/evidence\s+ext4", re.MULTILINE)
    assert fstab_regex.search(fstab_content), "fstab does not contain the correct entry for /app/evidence.img."

def test_drop_count():
    """Verify the drop count file contains the expected value."""
    drop_count_file = "/home/user/drop_count.txt"
    assert os.path.isfile(drop_count_file), f"{drop_count_file} does not exist."

    with open(drop_count_file, "r") as f:
        content = f.read().strip()

    assert content == "17", f"Expected drop count to be '17', but got '{content}'."

def test_adversarial_corpus():
    """Verify the log classifier script correctly identifies EVIL and CLEAN logs."""
    script_candidates = ["/home/user/classify_logs.py", "/home/user/classify_logs.sh"]
    script_path = None
    for p in script_candidates:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            script_path = p
            break

    assert script_path is not None, "Executable classify_logs script not found at /home/user/classify_logs.py or .sh"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_failures = []
    if os.path.isdir(evil_dir):
        for filename in os.listdir(evil_dir):
            filepath = os.path.join(evil_dir, filename)
            if os.path.isfile(filepath):
                result = subprocess.run([script_path, filepath], capture_output=True, text=True)
                if result.stdout.strip() != "EVIL":
                    evil_failures.append(filename)

    clean_failures = []
    if os.path.isdir(clean_dir):
        for filename in os.listdir(clean_dir):
            filepath = os.path.join(clean_dir, filename)
            if os.path.isfile(filepath):
                result = subprocess.run([script_path, filepath], capture_output=True, text=True)
                if result.stdout.strip() != "CLEAN":
                    clean_failures.append(filename)

    error_msg = ""
    if evil_failures:
        error_msg += f"{len(evil_failures)} evil bypassed: {', '.join(evil_failures)}. "
    if clean_failures:
        error_msg += f"{len(clean_failures)} clean modified/flagged: {', '.join(clean_failures)}."

    assert not evil_failures and not clean_failures, error_msg.strip()

def test_web_server():
    """Verify the web server is running in a container and serves the correct content over HTTPS."""
    # Check if container is running
    result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    if "alert-web" not in result.stdout:
        result = subprocess.run(["podman", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    assert "alert-web" in result.stdout, "Container 'alert-web' is not running."

    # Check web server response
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://localhost:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to connect to https://localhost:8443/: {e}")

    assert "CRITICAL_ALERT: 17" in content, f"Expected 'CRITICAL_ALERT: 17' in web server response, but got: {content}"