# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"

def run_detector(filepath):
    """Runs the detector script on the given file and returns its output lines."""
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, filepath],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().splitlines()

def test_detector_exists():
    """Ensure the student has created the detector script at the expected location."""
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def test_evil_corpus_rejection():
    """
    Iterate over every file in the evil corpus path.
    Assert the agent's solution rejects (flags as EVIL) each line.
    """
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) 
                  if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert evil_files, "No files found in evil corpus directory."

    bypassed_files = []
    total_evil_files = len(evil_files)

    for filepath in evil_files:
        with open(filepath, 'r') as f:
            expected_lines = sum(1 for _ in f)

        output_lines = run_detector(filepath)

        if len(output_lines) != expected_lines:
            bypassed_files.append(os.path.basename(filepath))
            continue

        misclassified = sum(1 for out in output_lines if out.strip() != "EVIL")
        if misclassified > 0:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {total_evil_files} evil bypassed. "
                    f"Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus_preservation():
    """
    Iterate over every file in the clean corpus path.
    Assert the agent's solution accepts (flags as CLEAN) each line.
    """
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) 
                   if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert clean_files, "No files found in clean corpus directory."

    modified_files = []
    total_clean_files = len(clean_files)

    for filepath in clean_files:
        with open(filepath, 'r') as f:
            expected_lines = sum(1 for _ in f)

        output_lines = run_detector(filepath)

        if len(output_lines) != expected_lines:
            modified_files.append(os.path.basename(filepath))
            continue

        misclassified = sum(1 for out in output_lines if out.strip() != "CLEAN")
        if misclassified > 0:
            modified_files.append(os.path.basename(filepath))

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {total_clean_files} clean modified. "
                    f"Offending files: {', '.join(modified_files)}")