# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/filter_data.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_adversarial_corpus():
    script_path = "/home/user/filter_data.sh"

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clean_modified = []
    evil_bypassed = []

    for c_file in clean_files:
        with open(c_file, "r") as f:
            # Sort lines to be robust against row reordering, though the task implies streaming processing
            expected_lines = sorted([line.strip() for line in f.readlines() if line.strip()])

        result = subprocess.run([script_path, c_file], capture_output=True, text=True)
        actual_lines = sorted([line.strip() for line in result.stdout.splitlines() if line.strip()])

        # In clean corpus, all rows should be preserved exactly
        if actual_lines != expected_lines:
            clean_modified.append(os.path.basename(c_file))

    for e_file in evil_files:
        result = subprocess.run([script_path, e_file], capture_output=True, text=True)
        actual_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        # In evil corpus, all rows should be rejected (empty output)
        if len(actual_lines) > 0:
            evil_bypassed.append(os.path.basename(e_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_final_output_exists():
    final_output_path = "/home/user/final_output.csv"
    assert os.path.isfile(final_output_path), f"Final output {final_output_path} is missing."