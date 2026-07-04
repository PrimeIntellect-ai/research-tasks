# test_final_state.py
import os
import subprocess
import pytest

def test_video_anomaly_detection():
    timestamps_file = "/home/user/red_alert_timestamps.txt"
    assert os.path.exists(timestamps_file), f"Missing {timestamps_file}"

    with open(timestamps_file, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected = ["14", "15", "16", "42", "43"]

    assert set(lines) == set(expected), f"Expected timestamps {expected}, but got {lines}"

def test_webhook_sanitizer_binary_exists():
    binary_path = "/home/user/alert_filter"
    assert os.path.exists(binary_path), f"Binary {binary_path} does not exist"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable"

def test_webhook_sanitizer_adversarial_corpus():
    binary_path = "/home/user/alert_filter"
    evil_corpus = "/app/corpus/evil"
    clean_corpus = "/app/corpus/clean"

    # Check evil files
    evil_files = [os.path.join(evil_corpus, f) for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]
    evil_failures = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(f))

    # Check clean files
    clean_files = [os.path.join(clean_corpus, f) for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]
    clean_failures = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    error_msg = []
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not error_msg, " | ".join(error_msg)

def test_filesystem_and_vault_setup():
    img_path = "/home/user/vault.img"
    mount_point = "/home/user/vault_mount"
    proxy_cache = "/home/user/proxy_cache"
    alerts_symlink = os.path.join(proxy_cache, "alerts")
    metrics_dir = os.path.join(proxy_cache, "metrics")
    logs_dir = os.path.join(proxy_cache, "logs")
    fstab_file = "/home/user/vault_fstab"

    assert os.path.exists(img_path), f"Missing {img_path}"

    # Check if formatted as ext4
    result = subprocess.run(["blkid", "-o", "value", "-s", "TYPE", img_path], capture_output=True, text=True)
    assert result.stdout.strip() == "ext4", f"{img_path} is not formatted as ext4"

    assert os.path.isdir(mount_point), f"Missing mount point {mount_point}"
    assert os.path.isdir(metrics_dir), f"Missing metrics dir {metrics_dir}"
    assert os.path.isdir(logs_dir), f"Missing logs dir {logs_dir}"

    assert os.path.islink(alerts_symlink), f"{alerts_symlink} is not a symlink"
    target = os.readlink(alerts_symlink)
    assert target == "/home/user/vault_mount/alerts", f"Symlink target is {target}, expected /home/user/vault_mount/alerts"

    assert os.path.exists(fstab_file), f"Missing {fstab_file}"
    with open(fstab_file, "r") as f:
        fstab_content = f.read().strip().split()

    assert len(fstab_content) >= 6, "fstab line format is incorrect"
    assert fstab_content[0] == "/home/user/vault.img", f"Incorrect fstab device: {fstab_content[0]}"
    assert fstab_content[1] == "/home/user/vault_mount", f"Incorrect fstab mount point: {fstab_content[1]}"
    assert fstab_content[2] == "ext4", f"Incorrect fstab fs type: {fstab_content[2]}"
    assert "loop" in fstab_content[3].split(","), f"Missing loop option in fstab: {fstab_content[3]}"