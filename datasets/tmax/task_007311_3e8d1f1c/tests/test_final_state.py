# test_final_state.py

import os
import pytest

def test_indexer_cpp_exists():
    assert os.path.isfile("/home/user/indexer.cpp"), "/home/user/indexer.cpp does not exist."

def test_indexer_binary_exists_and_executable():
    assert os.path.isfile("/home/user/indexer"), "/home/user/indexer binary does not exist."
    assert os.access("/home/user/indexer", os.X_OK), "/home/user/indexer is not executable."

def test_manifest_content():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"{manifest_path} does not exist."

    expected_lines = [
        "5d8c6b12a0d9237c72479e0aebc19cb9f816436bd32f3ea0a86d26f2849be5b5  section1/api.txt.gz",
        "c860c042918805f257a0cdcb7f18dbda093cd0c97801cdcd1ea22b2b1fb2d02c  section2/changelog.txt.gz"
    ]

    with open(manifest_path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Manifest content does not match expected.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )