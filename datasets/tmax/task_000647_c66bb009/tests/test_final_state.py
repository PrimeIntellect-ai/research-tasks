# test_final_state.py

import os
import json
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitiser.py"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
OUTPUT_FILE = "/tmp/output.json"

def run_sanitiser(input_dir, output_file):
    assert os.path.isfile(SCRIPT_PATH), f"Sanitiser script not found at {SCRIPT_PATH}"
    cmd = ["python3", SCRIPT_PATH, "--input_dir", input_dir, "--output_file", output_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.isfile(output_file), f"Output JSON file not created at {output_file}"

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_file} is not valid JSON.")

    # clean up the output file for the next run
    os.remove(output_file)
    return data

def test_clean_corpus_classification():
    """Test that all files in the clean corpus are classified as 'clean'."""
    clean_files = [os.path.basename(f) for f in glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.npy"))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    output_data = run_sanitiser(CLEAN_CORPUS_DIR, OUTPUT_FILE)

    failed_files = []
    for f in clean_files:
        if f not in output_data:
            failed_files.append(f"{f} (missing)")
        elif output_data[f] != "clean":
            failed_files.append(f"{f} (classified as {output_data[f]})")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_files)}")

def test_evil_corpus_classification():
    """Test that all files in the evil corpus are classified as 'evil'."""
    evil_files = [os.path.basename(f) for f in glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.npy"))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    output_data = run_sanitiser(EVIL_CORPUS_DIR, OUTPUT_FILE)

    failed_files = []
    for f in evil_files:
        if f not in output_data:
            failed_files.append(f"{f} (missing)")
        elif output_data[f] != "evil":
            failed_files.append(f"{f} (classified as {output_data[f]})")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {', '.join(failed_files)}")