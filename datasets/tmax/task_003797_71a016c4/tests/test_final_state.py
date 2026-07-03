# test_final_state.py

import os
import subprocess
import pytest
import glob

def run_script_on_file(script_path, file_path):
    try:
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return str(e)

def test_query_filter_script_exists():
    script_path = "/home/user/query_filter.py"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Not a file: {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/query_filter.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.sql"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.sql"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    evil_bypassed = []
    clean_modified = []

    for file_path in evil_files:
        output = run_script_on_file(script_path, file_path)
        if "REJECT" not in output or "ACCEPT" in output:
            evil_bypassed.append(os.path.basename(file_path))

    for file_path in clean_files:
        output = run_script_on_file(script_path, file_path)
        if "ACCEPT" not in output or "REJECT" in output:
            clean_modified.append(os.path.basename(file_path))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))