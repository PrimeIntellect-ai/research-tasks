# test_final_state.py

import os
import subprocess
import pytest

def test_validate_logs_clean_corpus():
    """Verify that the script correctly validates clean logs."""
    script_path = "/home/user/validate_logs.py"
    assert os.path.exists(script_path), f"Script not found: {script_path}"

    clean_corpus_dir = "/app/eval_corpus/clean"
    assert os.path.isdir(clean_corpus_dir), f"Clean corpus directory not found: {clean_corpus_dir}"

    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    failed_files = []
    for fpath in clean_files:
        result = subprocess.run(
            ["python3", script_path, fpath],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 or "VALID" not in result.stdout:
            failed_files.append(os.path.basename(fpath))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean files rejected or failed: {failed_files}"

def test_validate_logs_evil_corpus():
    """Verify that the script correctly rejects evil logs."""
    script_path = "/home/user/validate_logs.py"
    assert os.path.exists(script_path), f"Script not found: {script_path}"

    evil_corpus_dir = "/app/eval_corpus/evil"
    assert os.path.isdir(evil_corpus_dir), f"Evil corpus directory not found: {evil_corpus_dir}"

    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    failed_files = []
    for fpath in evil_files:
        result = subprocess.run(
            ["python3", script_path, fpath],
            capture_output=True,
            text=True
        )
        if result.returncode != 1 or "INVALID" not in result.stdout:
            failed_files.append(os.path.basename(fpath))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(evil_files)} evil files bypassed validation: {failed_files}"

def test_black_frames_count():
    """Verify the black frames count is correct."""
    count_file = "/home/user/black_frames_count.txt"
    assert os.path.exists(count_file), f"Black frames count file not found: {count_file}"

    with open(count_file, "r") as f:
        content = f.read().strip()

    try:
        student_count = int(content)
    except ValueError:
        pytest.fail(f"Content of {count_file} is not a valid integer: '{content}'")

    video_path = "/app/reference_video.mp4"
    assert os.path.exists(video_path), f"Reference video not found: {video_path}"

    # Recompute the expected count using ffmpeg
    cmd = f"ffmpeg -i {video_path} -vf blackframe -f null - 2>&1 | grep blackframe | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    try:
        expected_count = int(result.stdout.strip())
    except ValueError:
        pytest.fail("Failed to compute expected black frames count using ffmpeg.")

    assert student_count == expected_count, f"Expected {expected_count} black frames, but found {student_count} in {count_file}"