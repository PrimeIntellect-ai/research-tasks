# test_final_state.py
import os
import json
import re
import subprocess
import pytest

def test_script_exists():
    """Verify that the restore_filter.py script was created."""
    assert os.path.isfile("/home/user/restore_filter.py"), "Script /home/user/restore_filter.py does not exist."

def test_cron_job_exists_and_correct():
    """Verify that the cron job file exists and contains the correct schedule and command."""
    cron_path = "/home/user/backup_cron_job"
    assert os.path.isfile(cron_path), f"Cron job file {cron_path} does not exist."
    with open(cron_path, "r") as f:
        content = f.read()

    pattern = r"15\s+3\s+\*\s+\*\s+\*\s+.*python3\s+/home/user/restore_filter\.py\s+/home/user/incoming_backups\s+>\s+/home/user/backup_scan\.log"
    assert re.search(pattern, content), f"Cron job content does not match the expected schedule and command. Found: {content}"

def run_script_on_corpus(corpus_path):
    """Helper to run the user's script and parse its JSON output."""
    cmd = ["python3", "/home/user/restore_filter.py", corpus_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script timed out when running on {corpus_path}")

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    try:
        output_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Script output is not valid JSON. Output: {result.stdout}")

    return output_json

def test_adversarial_corpus_evil():
    """Verify that all files in the evil corpus are rejected (classified as 'evil')."""
    evil_corpus_path = "/app/corpus/evil"
    output = run_script_on_corpus(evil_corpus_path)

    expected_files = [f for f in os.listdir(evil_corpus_path) if f.endswith('.conf')]

    bypassed = []
    for f in expected_files:
        if output.get(f) != "evil":
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(expected_files)} evil bypassed: {', '.join(bypassed)}")

def test_adversarial_corpus_clean():
    """Verify that all files in the clean corpus are preserved (classified as 'clean')."""
    clean_corpus_path = "/app/corpus/clean"
    output = run_script_on_corpus(clean_corpus_path)

    expected_files = [f for f in os.listdir(clean_corpus_path) if f.endswith('.conf')]

    modified = []
    for f in expected_files:
        if output.get(f) != "clean":
            modified.append(f)

    if modified:
        pytest.fail(f"{len(modified)} of {len(expected_files)} clean modified: {', '.join(modified)}")