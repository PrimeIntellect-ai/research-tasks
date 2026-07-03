# test_final_state.py

import os
import subprocess
import pytest
import re

def test_sanitize_py_exists():
    """Test that the /home/user/sanitize.py script exists."""
    path = "/home/user/sanitize.py"
    assert os.path.exists(path), f"Missing script at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_adversarial_corpus():
    """Test the sanitize.py script against the clean and evil corpora."""
    script_path = "/home/user/sanitize.py"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(script_path), "sanitize.py is missing"
    assert os.path.exists(clean_dir), "clean corpus is missing"
    assert os.path.exists(evil_dir), "evil corpus is missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for f in clean_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not errors, "Corpus validation failed: " + "; ".join(errors)

def test_profile_env():
    """Test that DIAG_ENV=production is exported in .profile."""
    profile_path = "/home/user/.profile"
    assert os.path.exists(profile_path), f"Missing profile at {profile_path}"

    with open(profile_path, "r") as f:
        content = f.read()

    # Check for export DIAG_ENV=production or similar
    assert re.search(r"export\s+DIAG_ENV=[\"']?production[\"']?", content) or \
           re.search(r"DIAG_ENV=[\"']?production[\"']?\s*\n\s*export\s+DIAG_ENV", content), \
           "DIAG_ENV=production is not correctly exported in /home/user/.profile"

def test_audit_script():
    """Test that audit.sh exists, is executable, and appends to audit.log."""
    script_path = "/home/user/audit.sh"
    log_path = "/home/user/audit.log"

    assert os.path.exists(script_path), f"Missing script at {script_path}"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    # Run the script
    subprocess.run([script_path], check=True)

    assert os.path.exists(log_path), f"Log file {log_path} was not created"
    with open(log_path, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, "Log file is empty, expected date output"

def test_cron_job():
    """Test that the cron job is configured to run every 5 minutes."""
    try:
        output = subprocess.check_output(["crontab", "-l"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab for user")

    lines = [line.strip() for line in output.splitlines() if line.strip() and not line.startswith("#")]

    found = False
    for line in lines:
        if "/home/user/audit.sh" in line:
            parts = line.split()
            if len(parts) >= 6 and parts[0] in ("*/5", "0,5,10,15,20,25,30,35,40,45,50,55"):
                found = True
                break

    assert found, "Could not find a valid 5-minute cron job for /home/user/audit.sh in crontab"