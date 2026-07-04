# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_SCRIPT = "/home/user/detector.py"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"

def test_detector_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def run_detector(filepath):
    result = subprocess.run(
        ["python3", DETECTOR_SCRIPT, filepath],
        capture_output=True,
        text=True,
        timeout=15
    )
    return result.stdout.strip().splitlines()

def test_detector_evil_corpus():
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert evil_files, f"No files found in evil corpus directory {EVIL_CORPUS_DIR}"

    total_lines = 0
    bypassed_lines = 0
    failed_files = []

    for filepath in evil_files:
        with open(filepath, 'r') as f:
            file_lines = f.read().splitlines()

        if not file_lines:
            continue

        total_lines += len(file_lines)
        outputs = run_detector(filepath)

        if len(outputs) != len(file_lines):
            bypassed_lines += len(file_lines)
            failed_files.append(f"{os.path.basename(filepath)} (output count mismatch)")
            continue

        for i, out in enumerate(outputs):
            if out.strip() != "EVIL":
                bypassed_lines += 1
                if filepath not in failed_files:
                    failed_files.append(os.path.basename(filepath))

    assert bypassed_lines == 0, f"{bypassed_lines} of {total_lines} evil lines bypassed detection. Offending files: {', '.join(set(failed_files))}"

def test_detector_clean_corpus():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert clean_files, f"No files found in clean corpus directory {CLEAN_CORPUS_DIR}"

    total_lines = 0
    modified_lines = 0
    failed_files = []

    for filepath in clean_files:
        with open(filepath, 'r') as f:
            file_lines = f.read().splitlines()

        if not file_lines:
            continue

        total_lines += len(file_lines)
        outputs = run_detector(filepath)

        if len(outputs) != len(file_lines):
            modified_lines += len(file_lines)
            failed_files.append(f"{os.path.basename(filepath)} (output count mismatch)")
            continue

        for i, out in enumerate(outputs):
            if out.strip() != "CLEAN":
                modified_lines += 1
                if filepath not in failed_files:
                    failed_files.append(os.path.basename(filepath))

    assert modified_lines == 0, f"{modified_lines} of {total_lines} clean lines misclassified. Offending files: {', '.join(set(failed_files))}"