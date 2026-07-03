# test_final_state.py

import os
import subprocess
import pytest

def get_actual_video_duration(video_path):
    """Use ffprobe to get the actual duration of the video."""
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return float(result.stdout.strip())

def test_video_duration_extracted():
    """Check if the video duration was correctly extracted and saved."""
    output_file = "/home/user/video_duration.txt"
    video_file = "/app/test_video.mp4"

    assert os.path.exists(output_file), f"Output file missing: {output_file}"

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content, f"Output file {output_file} is empty."

    try:
        student_duration = float(content)
    except ValueError:
        pytest.fail(f"Content of {output_file} is not a valid number: '{content}'")

    expected_duration = get_actual_video_duration(video_file)

    # Allow a small tolerance for floating point formatting differences
    assert abs(student_duration - expected_duration) < 0.05, \
        f"Duration mismatch. Expected ~{expected_duration}, got {student_duration}"

def test_filter_executable_exists():
    """Check if the C++ filter program was compiled to the correct location."""
    filter_path = "/home/user/filter"
    assert os.path.exists(filter_path), f"Filter executable missing at {filter_path}"
    assert os.access(filter_path, os.X_OK), f"Filter at {filter_path} is not executable"

def test_adversarial_corpus_filter():
    """Test the filter against the clean and evil corpora."""
    filter_path = "/home/user/filter"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    # Check if valgrind is available to test for memory leaks
    valgrind_available = subprocess.run(["which", "valgrind"], stdout=subprocess.PIPE).returncode == 0

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failed = []
    evil_failed = []

    def run_filter(filepath):
        cmd = []
        if valgrind_available:
            # Use valgrind to catch memory leaks/errors. 
            # --error-exitcode=255 ensures valgrind returns 255 if a memory error is detected.
            cmd.extend(["valgrind", "--leak-check=full", "--error-exitcode=255", "--quiet"])
        cmd.extend([filter_path, filepath])

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1.0)
            return result.returncode, result.stderr.decode('utf-8')
        except subprocess.TimeoutExpired:
            return -1, "Timeout (infinite loop)"

    # Test clean corpus (Expected exit code 0)
    for c_file in clean_files:
        code, stderr = run_filter(c_file)
        if code != 0:
            basename = os.path.basename(c_file)
            reason = "Memory Leak/Crash" if code == 255 else f"Exit code {code}"
            clean_failed.append(f"{basename} ({reason})")

    # Test evil corpus (Expected exit code 1)
    for e_file in evil_files:
        code, stderr = run_filter(e_file)
        if code != 1:
            basename = os.path.basename(e_file)
            reason = "Memory Leak/Crash" if code == 255 else f"Exit code {code}"
            evil_failed.append(f"{basename} ({reason})")

    # Surface clear summary on failure
    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/failed: {', '.join(evil_failed)}")

    if error_messages:
        pytest.fail("\n".join(error_messages))