# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_filter_executable_exists():
    executable = "/home/user/filter"
    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_adversarial_corpus_evaluation():
    executable = "/home/user/filter"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.txt"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.txt"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([executable, f], capture_output=True, text=True)
        if "ACCEPT" not in result.stdout.strip():
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([executable, f], capture_output=True, text=True)
        if "REJECT" not in result.stdout.strip():
            evil_failed.append(os.path.basename(f))

    error_msg = []
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(clean_failed)}")
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(evil_failed)}")

    assert not clean_failed and not evil_failed, " | ".join(error_msg)

def test_rejected_frames_file():
    output_file = "/home/user/rejected_frames.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        lines = f.read().strip().split('\n')

    # Expected rejected frames based on truth
    expected_frames = ["15", "16", "17", "50", "85"]

    actual_frames = [line.strip() for line in lines if line.strip()]

    assert actual_frames == expected_frames, f"Expected rejected frames {expected_frames}, but got {actual_frames}."

def test_cond_plot_exists():
    plot_file = "/home/user/cond_plot.png"
    assert os.path.isfile(plot_file), f"Plot file {plot_file} does not exist."