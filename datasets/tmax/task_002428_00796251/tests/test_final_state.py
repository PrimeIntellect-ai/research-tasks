# test_final_state.py

import os
import difflib
import pytest

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except Exception:
        return ""

def test_recover_script_exists():
    script_path = "/home/user/recover.sh"
    assert os.path.isfile(script_path), f"Missing required script: {script_path}"

def test_compiled_docs_archive_exists():
    archive_path = "/app/compiled_docs.tar.xz"
    assert os.path.isfile(archive_path), f"Missing required archive: {archive_path}"

def test_compiled_docs_content_accuracy():
    compiled_path = "/app/compiled_docs.txt"
    assert os.path.isfile(compiled_path), f"Missing required file: {compiled_path}"

    expected = """SECURITY-CLASSIFICATION: TOP-SECRET-AURA
System Overview
Core logic goes here.
SECURITY-CLASSIFICATION: TOP-SECRET-AURA
API Endpoints
New v2 endpoint is active."""

    expected_alt = """SECURITY-CLASSIFICATION: TOP-SECRET-AURA
API Endpoints
New v2 endpoint is active.
SECURITY-CLASSIFICATION: TOP-SECRET-AURA
System Overview
Core logic goes here."""

    actual = read_file(compiled_path)

    score1 = difflib.SequenceMatcher(None, expected, actual).ratio()
    score2 = difflib.SequenceMatcher(None, expected_alt, actual).ratio()

    best_score = max(score1, score2)

    assert best_score >= 0.95, f"Content similarity score {best_score:.4f} is below the 0.95 threshold. Actual content:\n{actual}"