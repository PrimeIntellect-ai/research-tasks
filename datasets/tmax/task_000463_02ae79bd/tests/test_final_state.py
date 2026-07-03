# test_final_state.py

import os
import subprocess
import json
import pytest

def test_filter_clean_corpus():
    """Test that filter.py accepts all clean emails and outputs valid JSON."""
    clean_dir = "/home/user/corpora/clean"
    filter_script = "/home/user/filter.py"

    assert os.path.isfile(filter_script), f"Missing file: {filter_script}"

    failed_files = []
    total_files = 0

    for filename in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, filename)
        if not os.path.isfile(filepath):
            continue

        total_files += 1
        with open(filepath, 'rb') as f:
            result = subprocess.run(
                ['/usr/bin/python3', filter_script],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        if result.returncode != 0:
            failed_files.append(filename)
            continue

        try:
            output = result.stdout.decode('utf-8').strip()
            data = json.loads(output)
            # Check for valid UTC ISO8601 timestamp
            # We assume the student outputs some timestamp field, usually 'timestamp' or 'date'
            # The prompt doesn't specify exact JSON schema, but it must be valid JSON with the timestamp.
            # We'll just ensure it parses as JSON and didn't fail.
        except Exception:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {total_files} clean modified/failed: {', '.join(failed_files)}"


def test_filter_evil_corpus():
    """Test that filter.py rejects all evil emails with exit code 1."""
    evil_dir = "/home/user/corpora/evil"
    filter_script = "/home/user/filter.py"

    assert os.path.isfile(filter_script), f"Missing file: {filter_script}"

    failed_files = []
    total_files = 0

    for filename in os.listdir(evil_dir):
        filepath = os.path.join(evil_dir, filename)
        if not os.path.isfile(filepath):
            continue

        total_files += 1
        with open(filepath, 'rb') as f:
            result = subprocess.run(
                ['/usr/bin/python3', filter_script],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        if result.returncode == 0:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {total_files} evil bypassed: {', '.join(failed_files)}"


def test_e2e_flow():
    """Test the end-to-end flow using the expect script and process_mail script."""
    exp_path = "/home/user/trigger_alert.exp"
    sh_path = "/home/user/process_mail.sh"
    db_path = "/home/user/dashboard_db.json"

    assert os.path.isfile(exp_path), f"Missing file: {exp_path}"
    assert os.path.isfile(sh_path), f"Missing file: {sh_path}"

    # 1. Run the expect script to trigger the alert
    exp_result = subprocess.run(['/usr/bin/expect', exp_path], capture_output=True)
    assert exp_result.returncode == 0, f"trigger_alert.exp failed: {exp_result.stderr.decode()}"

    # 2. Run the bash script to process the mail
    sh_result = subprocess.run(['/bin/bash', sh_path], capture_output=True)
    assert sh_result.returncode == 0, f"process_mail.sh failed: {sh_result.stderr.decode()}"

    # 3. Verify the dashboard database
    assert os.path.isfile(db_path), f"Missing file: {db_path} (dashboard did not receive data)"

    with open(db_path, 'r') as f:
        content = f.read()

    # The dashboard_db.json might be a list of objects or JSON lines.
    # We check if the expected metric and value are present.
    assert "cpu_load" in content, "Metric 'cpu_load' not found in dashboard_db.json"
    assert "0.85" in content, "Value 0.85 not found in dashboard_db.json"