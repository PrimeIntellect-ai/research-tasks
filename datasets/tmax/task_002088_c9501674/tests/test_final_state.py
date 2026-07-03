# test_final_state.py

import os
import pytest

def test_quarantine_file():
    bad_file_quarantine = "/home/user/pipeline/quarantine/file_37.enc"
    bad_file_data = "/home/user/pipeline/data/file_37.enc"

    assert os.path.isfile(bad_file_quarantine), f"The bad file was not moved to {bad_file_quarantine}"
    assert not os.path.exists(bad_file_data), f"The bad file still exists in {bad_file_data}, it should have been moved."

def test_summary_file_contents():
    summary_file = "/home/user/pipeline/out/summary.txt"

    assert os.path.isfile(summary_file), f"The summary file {summary_file} does not exist. Did you run the ingest script?"

    with open(summary_file, 'r') as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 1, f"Expected exactly 1 line in summary.txt, but found {len(lines)} lines. The state leakage might not be fixed."
    assert lines[0] == "file_15.enc: CRITICAL", f"Expected 'file_15.enc: CRITICAL' in summary.txt, but got '{lines[0]}'."

def test_ingest_script_modified():
    script_path = "/home/user/pipeline/ingest.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing"

    # We don't strictly assert the exact code change, but we ensure the script is executable
    # and the result is correct (tested in test_summary_file_contents).
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"