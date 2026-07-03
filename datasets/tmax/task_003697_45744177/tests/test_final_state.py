# test_final_state.py

import os
import glob
import subprocess
import re
import pytest

def test_benchmark_log():
    log_path = "/home/user/workspace/benchmark.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, 'r') as f:
        content = f.read().strip()

    # Try to extract a float from the content
    match = re.search(r"[-+]?\d*\.\d+|\d+", content)
    assert match is not None, f"Could not find a valid float in {log_path}. Content: {content}"
    try:
        float(match.group())
    except ValueError:
        pytest.fail(f"Extracted value {match.group()} is not a valid float.")

def test_train_py_data_leakage_fixed():
    train_py_path = "/home/user/workspace/train.py"
    assert os.path.isfile(train_py_path), f"{train_py_path} does not exist."
    with open(train_py_path, 'r') as f:
        content = f.read()

    # Check that pca.fit is not called on the full dataset before split
    # A simple heuristic: look for pca.fit(X_train) or similar, and ensure pca.fit(X) is not there if split is after.
    # The prompt says: "verified by checking that pca.fit is called on X_train and not X"
    assert re.search(r"pca\.fit\(\s*X_train\s*\)", content) or re.search(r"pca\.fit_transform\(\s*X_train\s*\)", content), "pca.fit() is not called on X_train."
    assert not re.search(r"pca\.fit\(\s*X\s*\)", content) and not re.search(r"pca\.fit_transform\(\s*X\s*\)", content), "pca.fit() is still called on X (data leakage)."

def test_adversarial_corpus():
    detector_script = "/home/user/workspace/detector.py"
    assert os.path.isfile(detector_script), f"Detector script {detector_script} not found."

    evil_files = glob.glob("/app/corpus/evil/*.wav")
    clean_files = glob.glob("/app/corpus/clean/*.wav")

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for wav_file in evil_files:
        try:
            result = subprocess.run(
                ["python", detector_script, wav_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout.strip()
            if "EVIL" not in output:
                evil_bypassed.append((os.path.basename(wav_file), output))
        except Exception as e:
            evil_bypassed.append((os.path.basename(wav_file), str(e)))

    for wav_file in clean_files:
        try:
            result = subprocess.run(
                ["python", detector_script, wav_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout.strip()
            if "CLEAN" not in output:
                clean_modified.append((os.path.basename(wav_file), output))
        except Exception as e:
            clean_modified.append((os.path.basename(wav_file), str(e)))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join([x[0] for x in evil_bypassed])}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified. Offending files: {', '.join([x[0] for x in clean_modified])}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msg)