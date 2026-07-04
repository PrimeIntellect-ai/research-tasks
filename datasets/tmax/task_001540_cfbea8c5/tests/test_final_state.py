# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_payloads():
    """
    Validates that the student successfully extracted the 3 hidden payloads
    from the QR codes in the video and saved them to the correct file.
    """
    path = "/home/user/recovered_payloads.txt"
    assert os.path.exists(path), f"Recovered payloads file is missing at {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_payloads = [
        "<sCrIpt>alert(document.domain)</script>",
        "admin' OR 1=1--",
        "\"><svg/onload=prompt(1)>"
    ]

    for payload in expected_payloads:
        assert payload in content, f"Missing expected payload in {path}: {payload}"

def test_detector_script_exists_and_executable():
    """
    Validates that the detector script was created and is executable.
    """
    path = "/home/user/detector.sh"
    assert os.path.exists(path), f"Detector script is missing at {path}"
    assert os.access(path, os.X_OK), f"Detector script at {path} is not marked as executable"

def test_adversarial_corpus():
    """
    Validates the detector script against the evil and clean corpora.
    Evil files must result in exit code 1.
    Clean files must result in exit code 0.
    """
    detector_path = "/home/user/detector.sh"
    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (expecting exit code 1)
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."
    for f in evil_files:
        file_path = os.path.join(evil_dir, f)
        with open(file_path, "rb") as stdin_f:
            res = subprocess.run(["bash", detector_path], stdin=stdin_f)
            if res.returncode != 1:
                evil_bypassed.append(f)

    # Test clean corpus (expecting exit code 0)
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."
    for f in clean_files:
        file_path = os.path.join(clean_dir, f)
        with open(file_path, "rb") as stdin_f:
            res = subprocess.run(["bash", detector_path], stdin=stdin_f)
            if res.returncode != 0:
                clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus verification failed:\n" + "\n".join(errors)