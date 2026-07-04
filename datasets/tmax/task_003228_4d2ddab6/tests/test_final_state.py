# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_blocked_ips():
    """Verify that the correct IPs were extracted from the video."""
    blocked_ips_path = "/home/user/blocked_ips.txt"
    assert os.path.exists(blocked_ips_path), f"File not found: {blocked_ips_path}"

    with open(blocked_ips_path, "r") as f:
        ips = {line.strip() for line in f if line.strip()}

    expected_ips = {"192.168.1.105", "10.0.0.52"}
    assert ips == expected_ips, f"Expected IPs {expected_ips}, but found {ips}"

def test_upload_filter_clean_corpus():
    """Verify that the upload filter accepts all clean files."""
    script_path = "/home/user/upload_filter.py"
    assert os.path.exists(script_path), f"Script not found: {script_path}"

    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert clean_files, f"No clean files found in {clean_dir}"

    failed_clean = []
    for f in clean_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean files rejected: {failed_clean}"

def test_upload_filter_evil_corpus():
    """Verify that the upload filter rejects all evil files."""
    script_path = "/home/user/upload_filter.py"
    assert os.path.exists(script_path), f"Script not found: {script_path}"

    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert evil_files, f"No evil files found in {evil_dir}"

    bypassed_evil = []
    for f in evil_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode == 0:
            bypassed_evil.append(os.path.basename(f))

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed: {bypassed_evil}"