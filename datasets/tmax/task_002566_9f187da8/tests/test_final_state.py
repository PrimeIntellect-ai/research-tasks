# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/api_filter.sh"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No files found in evil corpus"

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True, text=True)
        if result.returncode == 0:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed rejection: {', '.join(bypassed_files)}")

def test_clean_corpus_accepted_and_transformed():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)

        # Read the original JSON to compute expected transformation
        with open(filepath, 'r') as f:
            try:
                original_data = json.load(f)
            except json.JSONDecodeError:
                continue # Should be valid JSON in clean corpus

        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True, text=True)

        if result.returncode != 0:
            failed_files.append(f"{filename} (exit code {result.returncode})")
            continue

        try:
            output_data = json.loads(result.stdout)
        except json.JSONDecodeError:
            failed_files.append(f"{filename} (invalid JSON output)")
            continue

        # Basic schema checks for the transformed output
        if "account_uuid" not in output_data:
            failed_files.append(f"{filename} (missing account_uuid)")
            continue

        if not output_data["account_uuid"].startswith("UUID-"):
            failed_files.append(f"{filename} (invalid account_uuid format)")
            continue

        if "profile" in output_data:
            failed_files.append(f"{filename} (profile object not removed)")
            continue

        if "status" not in output_data:
            failed_files.append(f"{filename} (missing status at root)")
            continue

        if not isinstance(output_data["status"], bool):
            failed_files.append(f"{filename} (status is not a boolean)")
            continue

        if output_data.get("role") == "admin":
            failed_files.append(f"{filename} (role is admin)")
            continue

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files failed processing or transformation: {', '.join(failed_files)}")