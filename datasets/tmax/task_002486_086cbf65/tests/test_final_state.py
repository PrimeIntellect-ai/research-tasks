# test_final_state.py
import os
import subprocess
import pytest

def test_adversarial_corpus():
    script_path = "/home/user/filter_artifacts.py"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for cf in clean_files:
        target_file = os.path.join(clean_dir, cf)
        cmd = ["python", script_path, "--input", target_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "ACCEPT":
            clean_failures.append(cf)

    evil_failures = []
    for ef in evil_files:
        target_file = os.path.join(evil_dir, ef)
        cmd = ["python", script_path, "--input", target_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "REJECT":
            evil_failures.append(ef)

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))