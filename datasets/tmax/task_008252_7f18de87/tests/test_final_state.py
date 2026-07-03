# test_final_state.py

import os
import pytest

def test_flag_contents():
    """Test that the flag file contains the correct highest-entropy string."""
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"Missing file: {flag_path}"
    assert os.path.isfile(flag_path), f"Not a file: {flag_path}"

    with open(flag_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "zQ8#kP9!mB4$vX1&"
    assert content == expected_flag, f"Incorrect flag content. Expected '{expected_flag}', got '{content}'"

def test_candidates_file():
    """Test that the candidates file was generated and contains the valid extracted strings."""
    candidates_path = "/home/user/candidates.txt"
    assert os.path.exists(candidates_path), f"Missing file: {candidates_path}"
    assert os.path.isfile(candidates_path), f"Not a file: {candidates_path}"

    with open(candidates_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_strings = [
        "normal_string_123",
        "debug_log_started",
        "zQ8#kP9!mB4$vX1&"
    ]

    for expected in expected_strings:
        assert expected in lines, f"Missing expected extracted string '{expected}' in {candidates_path}"

def test_extractor_fixed():
    """Ensure extractor.py is still present and modified."""
    extractor_path = "/home/user/extractor.py"
    assert os.path.exists(extractor_path), f"Missing file: {extractor_path}"
    assert os.path.isfile(extractor_path), f"Not a file: {extractor_path}"