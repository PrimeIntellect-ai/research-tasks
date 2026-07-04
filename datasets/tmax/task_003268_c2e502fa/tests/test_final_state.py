# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_extracted_payload():
    """Verify that the student extracted the payload correctly."""
    payload_path = "/home/user/extracted_payload.elf"
    assert os.path.exists(payload_path), f"Extracted payload not found at {payload_path}"

    with open(payload_path, "rb") as f:
        data = f.read()

    # Check if it's an ELF file
    assert data.startswith(b"\x7fELF"), "Extracted file is not a valid ELF binary"

    # Check if it contains the expected path traversal payload string
    assert b"../../../../etc/shadow" in data, "Extracted payload does not contain the expected path traversal string"

def test_classifier_against_corpus():
    """Verify the classifier script against the adversarial corpus."""
    classifier_path = "/home/user/classifier.py"
    assert os.path.exists(classifier_path), f"Classifier script not found at {classifier_path}"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*.mp4"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.mp4"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    # Test against evil corpus
    for f in evil_files:
        try:
            result = subprocess.run(
                ["python3", classifier_path, f],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = result.stdout.strip()
            if output != "EVIL":
                evil_bypassed.append(os.path.basename(f))
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(f)} (Error: {str(e)})")

    # Test against clean corpus
    for f in clean_files:
        try:
            result = subprocess.run(
                ["python3", classifier_path, f],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append(os.path.basename(f))
        except Exception as e:
            clean_modified.append(f"{os.path.basename(f)} (Error: {str(e)})")

    error_messages = []
    if evil_bypassed:
        error_messages.append(
            f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}"
        )
    if clean_modified:
        error_messages.append(
            f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}"
        )

    if error_messages:
        pytest.fail(" | ".join(error_messages))