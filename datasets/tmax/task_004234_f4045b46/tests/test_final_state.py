# test_final_state.py

import os
import subprocess
import pytest

def test_audio_duration_extracted():
    """Verify that the audio duration was correctly extracted and saved."""
    duration_file = "/home/user/audio_duration.txt"
    audio_file = "/app/interview.wav"

    assert os.path.isfile(duration_file), f"Duration file is missing at {duration_file}"

    # Recompute the expected duration using ffprobe
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        audio_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    expected_duration = result.stdout.strip()

    with open(duration_file, "r") as f:
        actual_duration = f.read().strip()

    assert actual_duration == expected_duration, f"Expected duration {expected_duration}, but got {actual_duration} in {duration_file}"

def test_script_exists_and_executable():
    """Verify that the validate_record.sh script exists and is executable."""
    script_path = "/home/user/validate_record.sh"
    assert os.path.isfile(script_path), f"Script is missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_adversarial_corpus():
    """Verify the script correctly identifies clean and evil records."""
    script_path = "/home/user/validate_record.sh"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".json")]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".json")]

    clean_failures = []
    for f in clean_files:
        file_path = os.path.join(clean_dir, f)
        result = subprocess.run([script_path, file_path], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(f)

    evil_failures = []
    for f in evil_files:
        file_path = os.path.join(evil_dir, f)
        result = subprocess.run([script_path, file_path], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(f)

    errors = []
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (failed to return 0): {', '.join(clean_failures)}")
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (failed to return non-zero): {', '.join(evil_failures)}")

    assert not errors, " | ".join(errors)