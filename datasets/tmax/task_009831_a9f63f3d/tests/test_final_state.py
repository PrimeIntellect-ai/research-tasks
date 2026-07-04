# test_final_state.py

import os
import tarfile
import tempfile

def test_source_files_exist():
    """Verify that the required source files exist."""
    assert os.path.isfile("/home/user/math_eval/main.cpp"), "main.cpp is missing."
    assert os.path.isfile("/home/user/math_eval/Makefile"), "Makefile is missing."
    assert os.path.isfile("/home/user/math_eval/run_tests.sh"), "run_tests.sh is missing."

def test_artifact_exists_and_contains_files():
    """Verify that the artifact tarball exists and contains the correct files."""
    artifact_path = "/home/user/artifact.tar.gz"
    assert os.path.isfile(artifact_path), "artifact.tar.gz is missing."

    with tarfile.open(artifact_path, "r:gz") as tar:
        members = [m.name for m in tar.getmembers()]

        # Paths in tarball might be relative or absolute, but they must end with the file names.
        calc_tool_found = any(m.endswith("calc_tool") for m in members)
        test_output_found = any(m.endswith("test_output.txt") for m in members)

        assert calc_tool_found, "calc_tool binary not found in tarball."
        assert test_output_found, "test_output.txt not found in tarball."

def test_test_output_contents():
    """Verify that the test_output.txt inside the tarball has the correct computed values."""
    artifact_path = "/home/user/artifact.tar.gz"
    assert os.path.isfile(artifact_path), "artifact.tar.gz is missing."

    expected_output = [
        "6.0000",
        "333.3333",
        "40.0000",
        "39.7500"
    ]

    extracted_lines = []
    with tarfile.open(artifact_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.name.endswith("test_output.txt"):
                f = tar.extractfile(member)
                if f is not None:
                    content = f.read().decode('utf-8')
                    extracted_lines = [line.strip() for line in content.strip().split('\n')]
                break

    assert extracted_lines, "test_output.txt was empty or could not be read from the tarball."
    assert len(extracted_lines) == len(expected_output), f"Expected {len(expected_output)} lines, got {len(extracted_lines)}."

    for i, (actual, expected) in enumerate(zip(extracted_lines, expected_output)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."