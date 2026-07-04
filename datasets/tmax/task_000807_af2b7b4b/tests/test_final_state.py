# test_final_state.py

import os
import subprocess
import pytest

def test_services_integration():
    """Verify that the services are correctly configured and communicating."""
    verify_script = "/app/verify_services.py"
    assert os.path.isfile(verify_script), f"{verify_script} not found."

    result = subprocess.run(["python3", verify_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Service verification failed. Output:\n{result.stdout}\n{result.stderr}"

def test_sanitizer_adversarial_corpus():
    """Verify the sanitizer script against the clean and evil corpora."""
    sanitizer_script = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_script), f"{sanitizer_script} is missing."

    evil_dir = "/home/user/corpus/evil"
    clean_dir = "/home/user/corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for ef in evil_files:
        res = subprocess.run(["python3", sanitizer_script, ef], capture_output=True)
        # Evil files should be rejected (exit code 1)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    for cf in clean_files:
        res = subprocess.run(["python3", sanitizer_script, cf], capture_output=True)
        # Clean files should be accepted (exit code 0)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))