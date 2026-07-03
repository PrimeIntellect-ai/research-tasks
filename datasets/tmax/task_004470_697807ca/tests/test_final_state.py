# test_final_state.py

import os
import difflib
import pytest

def test_final_documentation_similarity():
    target_path = "/home/user/final_documentation.md"
    golden_path = "/tmp/golden_documentation.md"

    assert os.path.exists(target_path), f"Output file missing: {target_path}"

    with open(target_path, "r", encoding="utf-8") as f:
        target = f.read().strip()

    if os.path.exists(golden_path):
        with open(golden_path, "r", encoding="utf-8") as f:
            golden = f.read().strip()
    else:
        # Fallback to the expected truth if the golden file is not present in the environment
        golden = "Welcome to NovaTech.\n\nNovaTech is great!"

    ratio = difflib.SequenceMatcher(None, target, golden).ratio()
    assert ratio >= 0.98, f"Similarity ratio {ratio:.4f} is below threshold 0.98.\n\nTarget content:\n{target}\n\nExpected content:\n{golden}"