# test_final_state.py
import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/sanitize.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def run_script_on_file(filepath):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, filepath],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split('\n')

def count_lines(filepath):
    with open(filepath, 'r') as f:
        return sum(1 for line in f if line.strip())

def test_sanitize_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_clean_corpus():
    clean_files = [f for f in glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*")) if os.path.isfile(f)]
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}"

    total_clean_lines = 0
    modified_clean_lines = 0
    offending_files = []

    for filepath in clean_files:
        lines_in_file = count_lines(filepath)
        if lines_in_file == 0:
            continue

        total_clean_lines += lines_in_file

        output_lines = run_script_on_file(filepath)
        output_lines = [line.strip() for line in output_lines if line.strip()]

        assert len(output_lines) == lines_in_file, f"Output length mismatch for {filepath}. Expected {lines_in_file} lines, got {len(output_lines)}."

        bad_count = sum(1 for out in output_lines if out != "CLEAN")
        if bad_count > 0:
            modified_clean_lines += bad_count
            offending_files.append(os.path.basename(filepath))

    if modified_clean_lines > 0:
        pytest.fail(f"{modified_clean_lines} of {total_clean_lines} clean modified. Offending files: {', '.join(set(offending_files))}")

def test_evil_corpus():
    evil_files = [f for f in glob.glob(os.path.join(EVIL_CORPUS_DIR, "*")) if os.path.isfile(f)]
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}"

    total_evil_lines = 0
    bypassed_evil_lines = 0
    offending_files = []

    for filepath in evil_files:
        lines_in_file = count_lines(filepath)
        if lines_in_file == 0:
            continue

        total_evil_lines += lines_in_file

        output_lines = run_script_on_file(filepath)
        output_lines = [line.strip() for line in output_lines if line.strip()]

        assert len(output_lines) == lines_in_file, f"Output length mismatch for {filepath}. Expected {lines_in_file} lines, got {len(output_lines)}."

        bad_count = sum(1 for out in output_lines if out != "EVIL")
        if bad_count > 0:
            bypassed_evil_lines += bad_count
            offending_files.append(os.path.basename(filepath))

    if bypassed_evil_lines > 0:
        pytest.fail(f"{bypassed_evil_lines} of {total_evil_lines} evil bypassed. Offending files: {', '.join(set(offending_files))}")