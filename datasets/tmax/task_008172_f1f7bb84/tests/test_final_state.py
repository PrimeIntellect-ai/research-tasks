# test_final_state.py
import os
import pytest

def test_result_log_exists_and_correct():
    result_path = "/home/user/result.log"
    assert os.path.isfile(result_path), f"Expected output file {result_path} does not exist. Ensure you compiled and ran the C application."

    with open(result_path, "r") as f:
        content = f.read()

    expected = "Migration to Python 3 complete! Protocol buffers and semver decoded."

    # Strip trailing newlines just in case the student added one during the C write
    actual = content.rstrip('\r\n')

    assert actual == expected, (
        f"File content mismatch in {result_path}.\n"
        f"Expected: '{expected}'\n"
        f"Got: '{actual}'\n"
        "Check your base64 decoding and semver comparison logic."
    )

def test_cmakelists_fixed():
    cmakelists_path = "/home/user/workspace/CMakeLists.txt"
    assert os.path.isfile(cmakelists_path), f"File {cmakelists_path} is missing."

    with open(cmakelists_path, "r") as f:
        content = f.read()

    assert "target_link_libraries" in content, (
        "CMakeLists.txt does not contain 'target_link_libraries'. "
        "The linker error must be fixed by linking against the protobuf-c library."
    )