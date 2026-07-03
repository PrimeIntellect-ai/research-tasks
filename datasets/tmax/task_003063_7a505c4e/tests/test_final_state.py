# test_final_state.py

import os
import sys
import subprocess
import pytest
from pathlib import Path

def test_part1_extractor_retry_bug():
    """
    Test that the vendored package bug is fixed.
    When SIMULATE_FLAKE=1, extract() should not produce duplicate records.
    """
    vendored_path = "/app/loctool-1.0.0"
    if vendored_path not in sys.path:
        sys.path.insert(0, vendored_path)

    try:
        from loctool.extractor import Extractor
    except ImportError:
        pytest.fail("Could not import loctool.extractor. Ensure the package is still intact.")

    os.environ["SIMULATE_FLAKE"] = "1"

    extractor = Extractor()
    input_data = {"key1": "value1", "key2": "value2", "key3": "value3"}

    try:
        output = extractor.extract(input_data)
    except Exception as e:
        pytest.fail(f"Extractor.extract() raised an exception: {e}")

    assert len(output) == len(input_data), (
        f"Expected output length {len(input_data)}, but got {len(output)}. "
        "The retry logic might still be appending to the records list without clearing previous attempts."
    )

def test_part2_quality_gate_adversarial_corpus():
    """
    Test the validate.py script against the adversarial corpus.
    Must accept 100% of clean translations and reject 100% of evil translations.
    """
    script_path = "/home/user/validate.py"
    assert os.path.exists(script_path), f"Quality gate script missing: {script_path}"

    source_file = "/app/corpora/source.json"
    clean_dir = Path("/app/corpora/clean")
    evil_dir = Path("/app/corpora/evil")

    assert clean_dir.exists() and clean_dir.is_dir(), "Clean corpus directory missing."
    assert evil_dir.exists() and evil_dir.is_dir(), "Evil corpus directory missing."

    clean_files = list(clean_dir.glob("*.json"))
    evil_files = list(evil_dir.glob("*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    evil_bypassed = []

    # Test clean corpus
    for target_file in clean_files:
        result = subprocess.run(
            ["python3", script_path, "--source", source_file, "--target", str(target_file)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            clean_failures.append(target_file.name)

    # Test evil corpus
    for target_file in evil_files:
        result = subprocess.run(
            ["python3", script_path, "--source", source_file, "--target", str(target_file)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            evil_bypassed.append(target_file.name)

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))