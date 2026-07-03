# test_final_state.py

import os
import glob
import subprocess
import csv
import pytest

def test_setup_py_fixed():
    setup_path = '/app/datacleaner/setup.py'
    assert os.path.exists(setup_path), f"File {setup_path} is missing."
    with open(setup_path, 'r') as f:
        content = f.read()
    assert 'broken-dep-123' not in content, "The invalid dependency 'broken-dep-123' was not removed from setup.py"

def test_filter_script_exists():
    script_path = '/home/user/filter.py'
    assert os.path.exists(script_path), f"Script {script_path} is missing."

def test_adversarial_corpus_filtering(tmp_path):
    script_path = '/home/user/filter.py'
    assert os.path.exists(script_path), f"Script {script_path} is missing."

    evil_files = glob.glob('/verifier/evil/*.csv')
    clean_files = glob.glob('/verifier/clean/*.csv')

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        output_file = tmp_path / f"out_evil_{os.path.basename(evil_file)}"
        cmd = ["python", script_path, "--input", evil_file, "--output", str(output_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on {evil_file}:\n{result.stderr}"

        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Output should only contain the header
        if len(rows) > 1:
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        output_file = tmp_path / f"out_clean_{os.path.basename(clean_file)}"
        cmd = ["python", script_path, "--input", clean_file, "--output", str(output_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on {clean_file}:\n{result.stderr}"

        with open(clean_file, 'r') as f:
            orig_rows = list(csv.reader(f))

        with open(output_file, 'r') as f:
            out_rows = list(csv.reader(f))

        if len(out_rows) != len(orig_rows):
            clean_modified.append(os.path.basename(clean_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))