# test_final_state.py
import os
import subprocess
import re
import pytest

OUTPUT_FILE = "/home/user/archived_segment.mp4"
CAMERA_FEED = "/app/camera_feed.mp4"
REFERENCE_FILE = "/tmp/reference_segment.mp4"
CPP_FILE = "/home/user/archiver.cpp"

def test_cpp_program_exists():
    """Check if the C++ program was created at the specified path."""
    assert os.path.isfile(CPP_FILE), f"Fail: {CPP_FILE} does not exist."

def test_output_file_exists():
    """Check if the archived segment video was generated."""
    assert os.path.isfile(OUTPUT_FILE), f"Fail: {OUTPUT_FILE} does not exist."

def test_file_size_constraint():
    """Check if the archived segment is heavily compressed (<= 200,000 bytes)."""
    size = os.path.getsize(OUTPUT_FILE)
    assert size <= 200000, f"Fail: File size {size} bytes exceeds 200,000 bytes."

def test_ssim_metric():
    """Generate a reference segment and compute the SSIM metric to ensure quality threshold."""
    # Generate the reference segment using ffmpeg
    cmd_ref = [
        "ffmpeg", "-y", "-ss", "3", "-t", "4", "-i", CAMERA_FEED,
        "-vf", "format=gray,scale=iw/2:ih/2", "-c:v", "libx264", "-crf", "0", REFERENCE_FILE
    ]
    try:
        subprocess.run(cmd_ref, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        pytest.fail("Fail: Could not generate the reference segment using ffmpeg.")

    # Compute SSIM between reference and the agent's output
    cmd_ssim = [
        "ffmpeg", "-i", REFERENCE_FILE, "-i", OUTPUT_FILE,
        "-lavfi", "ssim", "-f", "null", "-"
    ]
    result = subprocess.run(cmd_ssim, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Parse SSIM score from ffmpeg output (which logs to stderr)
    match = re.search(r'All:([0-9.]+)', result.stderr)
    assert match is not None, "Fail: Could not parse SSIM score from ffmpeg output. Is the output file a valid video?"

    ssim_score = float(match.group(1))
    assert ssim_score >= 0.85, f"Fail: SSIM score {ssim_score} is below the threshold of 0.85."