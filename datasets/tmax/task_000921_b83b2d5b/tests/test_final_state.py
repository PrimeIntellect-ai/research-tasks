# test_final_state.py

import os
import re
import subprocess
import glob
import pytest

def test_downtime_frames_count():
    path = "/home/user/downtime_frames.txt"
    assert os.path.isfile(path), f"{path} does not exist"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "45", f"Expected downtime_frames.txt to contain '45', but got '{content}'"

def test_rust_classifier_adversarial_corpus():
    debug_bin = "/home/user/classifier/target/debug/classifier"
    release_bin = "/home/user/classifier/target/release/classifier"

    executable = None
    if os.path.isfile(debug_bin) and os.access(debug_bin, os.X_OK):
        executable = debug_bin
    elif os.path.isfile(release_bin) and os.access(release_bin, os.X_OK):
        executable = release_bin

    assert executable is not None, "Could not find compiled Rust classifier executable in target/debug or target/release"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([executable, f], capture_output=True, text=True)
        out = result.stdout.strip()
        if out != "CLEAN":
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([executable, f], capture_output=True, text=True)
        out = result.stdout.strip()
        if out != "EVIL":
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/flagged: {', '.join(clean_failures)}")

    assert not error_msgs, "Classifier failed: " + "; ".join(error_msgs)

def test_mail_image_size():
    img_path = "/home/user/mail.img"
    assert os.path.isfile(img_path), f"{img_path} does not exist"
    size = os.path.getsize(img_path)
    expected_size = 50 * 1024 * 1024
    assert size == expected_size, f"Expected {img_path} to be {expected_size} bytes, got {size}"

def test_fstab_line():
    fstab_path = "/home/user/fstab_line.txt"
    assert os.path.isfile(fstab_path), f"{fstab_path} does not exist"
    with open(fstab_path, "r") as f:
        content = f.read().strip()

    pattern = r"/home/user/mail\.img\s+/home/user/mail_backup\s+ext4\s+loop,?(defaults)?\s+0\s+0"
    assert re.search(pattern, content), f"fstab line in {fstab_path} does not match expected format. Got: {content}"

def test_mail_backup_dir():
    dir_path = "/home/user/mail_backup"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist"

def test_podman_container_running():
    result = subprocess.run(["podman", "ps", "--filter", "name=mail_spooler", "--format", "{{.Names}}"], capture_output=True, text=True)
    assert "mail_spooler" in result.stdout, "Container 'mail_spooler' is not running"

def test_podman_container_mount():
    result = subprocess.run(["podman", "inspect", "mail_spooler"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to inspect container 'mail_spooler'"

    import json
    data = json.loads(result.stdout)
    mounts = data[0].get("Mounts", [])

    found_mount = False
    for mount in mounts:
        if mount.get("Source") == "/home/user/mail_backup" and mount.get("Destination") == "/var/mail":
            found_mount = True
            break

    assert found_mount, "Container 'mail_spooler' does not have the correct bind mount from /home/user/mail_backup to /var/mail"