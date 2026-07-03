# test_final_state.py

import os
import re
import json
import subprocess
import tempfile
import pytest

def test_bashrc_exports():
    """
    Verify that the required timezone and locale are exported in /home/user/.bashrc.
    """
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"Missing required file: {bashrc_path}"

    with open(bashrc_path, "r") as f:
        content = f.read()

    tz_match = re.search(r'TZ\s*=\s*["\']?Europe/Berlin["\']?', content)
    lang_match = re.search(r'LANG\s*=\s*["\']?de_DE\.UTF-8["\']?', content)

    assert tz_match is not None, "TZ=Europe/Berlin not properly set in /home/user/.bashrc"
    assert lang_match is not None, "LANG=de_DE.UTF-8 not properly set in /home/user/.bashrc"

def test_crontab_setup():
    """
    Verify that the cron job is correctly scheduled for the 'user' account.
    """
    try:
        output = subprocess.check_output(["crontab", "-l", "-u", "user"], stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError:
        try:
            output = subprocess.check_output(["sudo", "-u", "user", "crontab", "-l"], stderr=subprocess.STDOUT).decode("utf-8")
        except subprocess.CalledProcessError:
            pytest.fail("Failed to read crontab for 'user'. Ensure the crontab exists.")

    expected_cmd = "python3 /home/user/config_auditor.py /opt/configs /home/user/audit_report.json"

    found = False
    for line in output.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Check if the command is present and the schedule is every 15 minutes
        if expected_cmd in line and line.startswith("*/15"):
            found = True
            break

    assert found, f"Cron job not found or incorrect schedule. Expected command: '{expected_cmd}' running every 15 minutes ('*/15 * * * *')."

def test_auditor_script_adversarial_corpus():
    """
    Verify the config_auditor.py script correctly classifies 'evil' and 'clean' files.
    """
    script_path = "/home/user/config_auditor.py"
    assert os.path.isfile(script_path), f"Auditing script not found at {script_path}"

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = os.listdir(evil_dir)
    clean_files = os.listdir(clean_dir)

    assert len(evil_files) > 0, "Evil corpus directory is empty"
    assert len(clean_files) > 0, "Clean corpus directory is empty"

    # Run script against evil corpus
    with tempfile.NamedTemporaryFile(suffix=".json") as evil_out:
        try:
            subprocess.run(["python3", script_path, evil_dir, evil_out.name], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Script execution failed on evil corpus:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

        try:
            with open(evil_out.name, "r") as f:
                evil_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output JSON from evil directory is invalid or empty.")

    # Run script against clean corpus
    with tempfile.NamedTemporaryFile(suffix=".json") as clean_out:
        try:
            subprocess.run(["python3", script_path, clean_dir, clean_out.name], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Script execution failed on clean corpus:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

        try:
            with open(clean_out.name, "r") as f:
                clean_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output JSON from clean directory is invalid or empty.")

    evil_bypassed = []
    for f in evil_files:
        if evil_results.get(f) != "evil":
            evil_bypassed.append(f)

    clean_modified = []
    for f in clean_files:
        if clean_results.get(f) != "clean":
            clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (flagged as evil or missing): {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))