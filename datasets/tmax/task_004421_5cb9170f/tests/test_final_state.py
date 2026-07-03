# test_final_state.py

import os
import subprocess
import pytest

def test_libsensordata_fixed():
    repo_path = "/app/libsensordata"
    # Ensure the library compiles and tests pass
    try:
        subprocess.run(["make"], cwd=repo_path, check=True, capture_output=True, text=True)
        subprocess.run(["make", "check"], cwd=repo_path, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to build or pass tests in {repo_path}. 'make check' failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

def test_detector_exists_and_executable():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable not found at {detector_path}."
    assert os.access(detector_path, os.X_OK), f"Detector at {detector_path} is not executable."

def test_detector_adversarial_corpus():
    detector_path = "/home/user/detector"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    failed_clean = []
    for f in clean_files:
        res = subprocess.run([detector_path, f], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        res = subprocess.run([detector_path, f], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(f))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil)}")

    if errors:
        pytest.fail(" | ".join(errors))