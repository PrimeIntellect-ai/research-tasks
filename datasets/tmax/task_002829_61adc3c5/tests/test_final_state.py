# test_final_state.py

import os
import subprocess
import pytest

def test_video_secret_extracted():
    """Check if the secret token was correctly extracted from the video."""
    secret_path = "/home/user/video_secret.txt"
    assert os.path.exists(secret_path), f"Secret file is missing at {secret_path}"

    with open(secret_path, "r") as f:
        content = f.read().strip()

    expected_token = "TOKEN:A7x9F2mP4vL8qR3w"
    assert content == expected_token, f"Extracted token is incorrect. Expected '{expected_token}', found '{content}'"

def test_adversarial_corpus_detection():
    """Check if the classifier correctly identifies evil and clean payloads."""
    # Find the detector script
    detector_path = None
    for ext in ["", ".py", ".sh", ".js", ".rb", ".pl"]:
        path = f"/home/user/detector{ext}"
        if os.path.exists(path):
            detector_path = path
            break

    assert detector_path is not None, "Could not find detector script at /home/user/detector.*"

    # Determine how to run the script
    cmd_prefix = []
    if not os.access(detector_path, os.X_OK):
        if detector_path.endswith('.py'):
            cmd_prefix = ['python3']
        elif detector_path.endswith('.sh'):
            cmd_prefix = ['bash']
        elif detector_path.endswith('.js'):
            cmd_prefix = ['node']
        else:
            pytest.fail(f"Detector script {detector_path} is not executable and has unknown extension.")

    # Test Evil Corpus
    evil_dir = "/app/corpus/evil/"
    assert os.path.exists(evil_dir), "Evil corpus directory is missing."
    evil_files = set(f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f)))
    total_evil = len(evil_files)

    cmd_evil = cmd_prefix + [detector_path, evil_dir]
    result_evil = subprocess.run(cmd_evil, capture_output=True, text=True)

    evil_bypassed = []
    for line in result_evil.stdout.splitlines():
        line = line.strip()
        if not line or ": " not in line: 
            continue
        filename, verdict = line.split(": ", 1)
        filename = os.path.basename(filename)

        if filename in evil_files:
            if verdict.strip() != "EVIL":
                evil_bypassed.append(filename)
            evil_files.remove(filename)

    # Any files not reported in standard output are considered bypassed/failed
    evil_bypassed.extend(list(evil_files))

    # Test Clean Corpus
    clean_dir = "/app/corpus/clean/"
    assert os.path.exists(clean_dir), "Clean corpus directory is missing."
    clean_files = set(f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f)))
    total_clean = len(clean_files)

    cmd_clean = cmd_prefix + [detector_path, clean_dir]
    result_clean = subprocess.run(cmd_clean, capture_output=True, text=True)

    clean_modified = []
    for line in result_clean.stdout.splitlines():
        line = line.strip()
        if not line or ": " not in line: 
            continue
        filename, verdict = line.split(": ", 1)
        filename = os.path.basename(filename)

        if filename in clean_files:
            if verdict.strip() != "CLEAN":
                clean_modified.append(filename)
            clean_files.remove(filename)

    # Any files not reported in standard output are considered modified/failed
    clean_modified.extend(list(clean_files))

    # Aggregate failures
    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {total_clean} clean modified/flagged: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)