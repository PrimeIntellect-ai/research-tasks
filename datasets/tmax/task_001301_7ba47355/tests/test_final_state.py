# test_final_state.py

import os
import subprocess
import pytest

def test_audit_filter_script_exists():
    script_path = "/home/user/audit_filter.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_adversarial_corpus():
    script_path = "/home/user/audit_filter.py"
    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    evil_files = sorted([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])
    clean_files = sorted([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])

    assert len(evil_files) > 0, "No files found in evil corpus"
    assert len(clean_files) > 0, "No files found in clean corpus"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (expected: LEAK)
    for ef in evil_files:
        file_path = os.path.join(evil_dir, ef)
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if result.returncode != 0 or output != "LEAK":
            evil_bypassed.append((ef, output, result.stderr))

    # Test clean corpus (expected: CLEAN)
    for cf in clean_files:
        file_path = os.path.join(clean_dir, cf)
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if result.returncode != 0 or output != "CLEAN":
            clean_modified.append((cf, output, result.stderr))

    error_messages = []
    if evil_bypassed:
        basenames = [item[0] for item in evil_bypassed]
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(basenames)}")

    if clean_modified:
        basenames = [item[0] for item in clean_modified]
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (failed to output CLEAN): {', '.join(basenames)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))