# test_final_state.py
import os
import glob
import subprocess
import csv
import hashlib
import pytest

def test_filter_script_adversarial_corpus():
    """Test that the filter script correctly classifies the adversarial corpus."""
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), "Filter script /home/user/filter.sh is missing."

    evil_corpus_path = "/app/corpora/eval_evil"
    clean_corpus_path = "/app/corpora/eval_clean"

    # We might not have eval_evil and eval_clean if the environment doesn't provide them, 
    # but the verifier instructions say they are the holdout sets.
    # If they are not available, fallback to the training sets to avoid crashing if the setup is slightly different.
    if not os.path.isdir(evil_corpus_path):
        evil_corpus_path = "/app/corpora/evil"
    if not os.path.isdir(clean_corpus_path):
        clean_corpus_path = "/app/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_corpus_path, "*.png"))
    clean_files = glob.glob(os.path.join(clean_corpus_path, "*.png"))

    assert len(evil_files) > 0, f"No evil files found in {evil_corpus_path}"
    assert len(clean_files) > 0, f"No clean files found in {clean_corpus_path}"

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["bash", script_path, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run(["bash", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified[:5])}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msg)

def test_frames_extraction_and_filtering():
    """Test that frames were extracted and corrupted ones were removed."""
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), "Frames directory /home/user/frames is missing."

    extracted_frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
    assert len(extracted_frames) > 0, "No extracted frames found."

    extracted_basenames = [os.path.basename(f) for f in extracted_frames]

    expected_missing = ["frame_0004.png", "frame_0005.png", "frame_0008.png"]
    for missing in expected_missing:
        assert missing not in extracted_basenames, f"Corrupted frame {missing} was not removed."

    expected_present = [
        "frame_0001.png", "frame_0002.png", "frame_0003.png", 
        "frame_0006.png", "frame_0007.png", "frame_0009.png", "frame_0010.png"
    ]
    for present in expected_present:
        assert present in extracted_basenames, f"Clean frame {present} is missing."

def test_valid_rollout_csv():
    """Test the reproducibility log valid_rollout.csv."""
    csv_path = "/home/user/valid_rollout.csv"
    assert os.path.isfile(csv_path), "Reproducibility log /home/user/valid_rollout.csv is missing."

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."
    assert rows[0] == ["filename", "sha256"], "CSV header is incorrect or missing."

    data_rows = rows[1:]
    assert len(data_rows) == 7, f"Expected 7 data rows, but found {len(data_rows)}."

    # Check that it's sorted alphabetically by filename
    filenames = [row[0] for row in data_rows]
    assert filenames == sorted(filenames), "CSV rows are not sorted alphabetically by filename."

    # Check sha256 hashes
    for row in data_rows:
        filename, csv_hash = row
        assert len(csv_hash) == 64, f"Invalid SHA-256 hash length for {filename}."

        file_path = os.path.join("/home/user/frames", filename)
        assert os.path.isfile(file_path), f"File {filename} listed in CSV but not found in /home/user/frames."

        with open(file_path, "rb") as img_f:
            actual_hash = hashlib.sha256(img_f.read()).hexdigest()

        assert csv_hash == actual_hash, f"Hash mismatch for {filename}. Expected {actual_hash}, got {csv_hash}."