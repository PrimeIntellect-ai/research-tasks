# test_final_state.py

import os
import json
import subprocess
import re
import pytest

ARCHIVE_DIR = "/home/user/archive"
ORIGINAL_VIDEO = "/app/surveillance.mp4"
RECONSTRUCTED = "/tmp/reconstructed.mp4"
LOG_FILE = "/home/user/dedup_log.json"

def test_archive_directory_and_chunks():
    """Verify that the archive directory exists and contains 60 chunks."""
    assert os.path.exists(ARCHIVE_DIR), f"Archive directory not found: {ARCHIVE_DIR}"
    assert os.path.isdir(ARCHIVE_DIR), f"Archive path is not a directory: {ARCHIVE_DIR}"

    chunks = sorted([f for f in os.listdir(ARCHIVE_DIR) if f.endswith('.mp4')])
    assert len(chunks) == 60, f"Expected 60 chunks in archive, found {len(chunks)}"

    # Check that chunks are named correctly
    for i in range(60):
        expected_name = f"chunk_{i:02d}.mp4"
        assert expected_name in chunks, f"Missing expected chunk: {expected_name}"

def test_log_file():
    """Verify that the deduplication log exists and is valid JSON."""
    assert os.path.exists(LOG_FILE), f"Log file not found: {LOG_FILE}"
    assert os.path.isfile(LOG_FILE), f"Log path is not a file: {LOG_FILE}"

    try:
        with open(LOG_FILE, 'r') as f:
            log_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Log file {LOG_FILE} is not valid JSON")

    assert isinstance(log_data, dict), "Log data must be a JSON dictionary"
    assert len(log_data) == 60, f"Expected 60 entries in log, found {len(log_data)}"

def test_deduplication_score():
    """Verify the fidelity (PSNR) and storage savings metric."""
    assert os.path.exists(ARCHIVE_DIR), f"Archive directory not found: {ARCHIVE_DIR}"

    chunks = sorted([f for f in os.listdir(ARCHIVE_DIR) if f.endswith('.mp4')])
    assert len(chunks) == 60, f"Expected 60 chunks in archive, found {len(chunks)}"

    concat_txt = "/tmp/concat.txt"
    with open(concat_txt, "w") as f:
        for chunk in chunks:
            f.write(f"file '{os.path.join(ARCHIVE_DIR, chunk)}'\n")

    # Reconstruct video
    concat_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
        "-i", concat_txt, "-c", "copy", RECONSTRUCTED
    ]
    subprocess.run(concat_cmd, capture_output=True, check=False)

    assert os.path.exists(RECONSTRUCTED), "Failed to reconstruct video from chunks"

    # Calculate PSNR
    psnr_cmd = [
        "ffmpeg", "-i", ORIGINAL_VIDEO, "-i", RECONSTRUCTED, 
        "-lavfi", "psnr", "-f", "null", "-"
    ]
    result = subprocess.run(psnr_cmd, capture_output=True, text=True)
    psnr_output = result.stderr

    psnr_val = 0.0
    match = re.search(r'average:([0-9.]+)', psnr_output)
    if match:
        psnr_val = float(match.group(1))
    elif 'average:inf' in psnr_output:
        psnr_val = 100.0
    else:
        pytest.fail(f"Could not parse PSNR from ffmpeg output: {psnr_output}")

    # Calculate physical disk size
    du_cmd = ["du", "-sb", ARCHIVE_DIR]
    du_result = subprocess.run(du_cmd, capture_output=True, text=True)
    try:
        size_bytes = int(du_result.stdout.split()[0])
    except (IndexError, ValueError):
        pytest.fail(f"Could not parse directory size from du output: {du_result.stdout}")

    size_mb = size_bytes / (1024 * 1024)
    expected_uncompressed_mb = 12.0
    ratio = min(size_mb / expected_uncompressed_mb, 1.0)

    score = psnr_val * (1.0 - ratio)

    assert score >= 20.0, (
        f"Metric threshold failed: Score {score:.2f} < 20.0. "
        f"PSNR: {psnr_val:.2f}, Size: {size_mb:.2f} MB"
    )