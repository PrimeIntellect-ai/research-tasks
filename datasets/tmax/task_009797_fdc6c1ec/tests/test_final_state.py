# test_final_state.py

import os
import re
import hashlib

def test_merger_c_exists_and_contains_flock():
    """Test that merger.c exists and uses flock() with LOCK_EX."""
    c_file = "/home/user/merger.c"
    assert os.path.isfile(c_file), f"File {c_file} does not exist."

    with open(c_file, 'r') as f:
        content = f.read()

    assert "flock" in content, f"{c_file} does not contain 'flock'."
    assert "LOCK_EX" in content, f"{c_file} does not contain 'LOCK_EX'."

def test_merged_tar_exists():
    """Test that merged.tar.gz was created."""
    merged_tar = "/home/user/repo/merged.tar.gz"
    assert os.path.isfile(merged_tar), f"File {merged_tar} does not exist."

def test_artifact_extracted():
    """Test that artifact.bin was extracted."""
    artifact = "/home/user/repo/artifact.bin"
    assert os.path.isfile(artifact), f"File {artifact} does not exist."

    with open(artifact, 'rb') as f:
        content = f.read()

    expected_content = b"CRITICAL_ARTIFACT_DATA_V1\n"
    assert content == expected_content, f"Contents of {artifact} do not match the expected data."

def test_curation_report():
    """Test that curation_report.txt exists and contains the correct SHA-256 hash."""
    report_file = "/home/user/curation_report.txt"
    assert os.path.isfile(report_file), f"File {report_file} does not exist."

    expected_hash = "f3411e809311029e0de55bba20bce32ba71ab73cebc4eb03eb0cd7631ccca17a"
    expected_line = f"Artifact SHA256: {expected_hash}"

    with open(report_file, 'r') as f:
        content = f.read().strip()

    assert content == expected_line, f"Contents of {report_file} are incorrect. Expected '{expected_line}', got '{content}'."