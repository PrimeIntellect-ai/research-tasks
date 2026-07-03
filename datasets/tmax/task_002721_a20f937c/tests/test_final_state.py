# test_final_state.py

import os
import subprocess
import pytest

def test_pyaes_is_fixed():
    aes_path = "/app/pyaes-1.6.1/pyaes/aes.py"
    assert os.path.exists(aes_path), f"The vendored pyaes file is missing at {aes_path}"
    with open(aes_path, "r") as f:
        content = f.read()
    assert "return (x ^ y)" in content and "return (x + y)" not in content, \
        "The perturbation in aes.py has not been correctly fixed. Expected bitwise XOR."

def test_detector_script_exists():
    detector_path = "/home/user/detector.py"
    assert os.path.exists(detector_path), f"The detector script {detector_path} is missing."
    assert os.path.isfile(detector_path), f"The path {detector_path} is not a file."

def test_adversarial_corpus_clean():
    detector_path = "/home/user/detector.py"
    clean_dir = "/app/corpora/clean/"
    assert os.path.exists(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in the clean corpus."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(
            ["python3", detector_path, filepath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "SAFE":
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/flagged incorrectly. Offending files: {', '.join(failed_files)}")

def test_adversarial_corpus_evil():
    detector_path = "/home/user/detector.py"
    evil_dir = "/app/corpora/evil/"
    assert os.path.exists(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in the evil corpus."

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(
            ["python3", detector_path, filepath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "EVIL":
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")