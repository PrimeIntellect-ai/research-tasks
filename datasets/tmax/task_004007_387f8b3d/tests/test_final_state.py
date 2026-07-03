# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_transcript_created_and_correct():
    transcript_path = "/home/user/transcript.txt"
    assert os.path.isfile(transcript_path), f"Transcript file {transcript_path} is missing."

    with open(transcript_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    # Whisper might transcribe numbers as digits or words. We check for either.
    content_no_hyphens = content.replace("-", " ")
    has_seed = "4294967295" in content or "four two nine four nine six seven two nine five" in content_no_hyphens
    has_boundary = "-1" in content or "negative one" in content_no_hyphens

    assert has_seed, "Transcript does not contain the correct seed value (4294967295 or its word equivalent)."
    assert has_boundary, "Transcript does not contain the correct boundary constraint (-1 or 'negative one')."

def test_fuzzer_recovered():
    fuzzer_path = "/home/user/fuzzer.sh"
    assert os.path.isfile(fuzzer_path), f"Recovered fuzzer script {fuzzer_path} is missing."

def test_detector_adversarial_corpus():
    detector_path = "/home/user/detector.sh"
    assert os.path.isfile(detector_path), f"Detector script {detector_path} is missing."

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = [f for f in glob.glob(os.path.join(evil_dir, "*")) if os.path.isfile(f)]
    clean_files = [f for f in glob.glob(os.path.join(clean_dir, "*")) if os.path.isfile(f)]

    assert len(evil_files) > 0, f"No files found in evil corpus directory {evil_dir}."
    assert len(clean_files) > 0, f"No files found in clean corpus directory {clean_dir}."

    bypassed_evil = []
    for evil_file in evil_files:
        result = subprocess.run(["bash", detector_path, evil_file], capture_output=True)
        # Evil files must be rejected with exit code 1
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(evil_file))

    modified_clean = []
    for clean_file in clean_files:
        result = subprocess.run(["bash", detector_path, clean_file], capture_output=True)
        # Clean files must be accepted with exit code 0
        if result.returncode != 0:
            modified_clean.append(os.path.basename(clean_file))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean rejected: {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))