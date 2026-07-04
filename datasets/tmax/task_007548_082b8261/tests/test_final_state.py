# test_final_state.py

import os
import pytest

def test_extracted_valid_sets():
    """Verify that only valid sets are extracted."""
    assert os.path.exists("/home/user/extracted/set1"), "set1 was not extracted"
    assert os.path.exists("/home/user/extracted/set2"), "set2 was not extracted"

    assert os.path.exists("/home/user/extracted/set1/sample_alpha.txt"), "sample_alpha.txt missing"
    assert os.path.exists("/home/user/extracted/set1/sample_alpha.dat"), "sample_alpha.dat missing"
    assert os.path.exists("/home/user/extracted/set2/sample_beta.txt"), "sample_beta.txt missing"
    assert os.path.exists("/home/user/extracted/set2/sample_beta.dat"), "sample_beta.dat missing"

def test_extracted_invalid_sets():
    """Verify that corrupted sets are not extracted."""
    assert not os.path.exists("/home/user/extracted/set3"), "set3 (corrupted) should not be extracted"

def test_symlinks_created():
    """Verify that the symlinks are correctly created in the organized directory."""
    symlink_rna = "/home/user/organized/RNA/X99.dat"
    symlink_dna = "/home/user/organized/DNA/M01.dat"

    assert os.path.islink(symlink_rna), f"{symlink_rna} is not a symlink or does not exist"
    assert os.path.islink(symlink_dna), f"{symlink_dna} is not a symlink or does not exist"

    target_rna = os.readlink(symlink_rna)
    target_dna = os.readlink(symlink_dna)

    assert target_rna.endswith("/home/user/extracted/set1/sample_alpha.dat") or target_rna == "../../extracted/set1/sample_alpha.dat", \
        f"{symlink_rna} points to wrong target: {target_rna}"
    assert target_dna.endswith("/home/user/extracted/set2/sample_beta.dat") or target_dna == "../../extracted/set2/sample_beta.dat", \
        f"{symlink_dna} points to wrong target: {target_dna}"

def test_success_log():
    """Verify the contents of the success log."""
    log_path = "/home/user/success.log"
    assert os.path.exists(log_path), f"{log_path} does not exist"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "DNA:M01",
        "RNA:X99"
    ]

    assert lines == expected_lines, f"Log contents are incorrect. Expected {expected_lines}, got {lines}"