# test_final_state.py
import os
import subprocess
import glob
import pytest
import re

def test_adversarial_corpus():
    script_path = "/home/user/validate_subs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.jsonl"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.jsonl"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        with open(cf, 'r') as f:
            expected_output = f.read().strip()

        result = subprocess.run([script_path, cf], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != expected_output:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True, text=True)
        # For pure evil files, it should either exit non-zero or output nothing
        if result.returncode == 0 and result.stdout.strip() != "":
            evil_failed.append(os.path.basename(ef))

    error_msg = []
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not error_msg, " | ".join(error_msg)

def test_srt_output():
    srt_path = "/home/user/final_subtitles.srt"
    assert os.path.isfile(srt_path), f"SRT file {srt_path} does not exist."

    with open(srt_path, "r") as f:
        content = f.read()

    expected_timestamps = [
        ("00:00:00,000", "00:00:03,500"),
        ("00:00:03,500", "00:00:07,200"),
        ("00:00:07,200", "00:00:12,200"),
        ("00:00:14,100", "00:00:15,000"),
    ]

    # Extract all timestamp lines
    timestamps = re.findall(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})", content)

    assert len(timestamps) == len(expected_timestamps), f"Expected {len(expected_timestamps)} subtitle blocks, found {len(timestamps)}."

    for i, (expected_start, expected_end) in enumerate(expected_timestamps):
        actual_start, actual_end = timestamps[i]
        assert actual_start == expected_start, f"Block {i+1} start time mismatch. Expected {expected_start}, got {actual_start}."
        assert actual_end == expected_end, f"Block {i+1} end time mismatch. Expected {expected_end}, got {actual_end}."

    # Check that the text lines are correct
    assert "Slide 1: Introduction" in content
    assert "Slide 2: Analytics" in content
    assert "Slide 3: Deep Dive" in content
    assert "Slide 4: Conclusion" in content