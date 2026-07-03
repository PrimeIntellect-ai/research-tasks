# test_final_state.py

import os
import hashlib
import pytest

def test_prep_config_script_exists():
    script_path = "/home/user/prep_config.sh"
    assert os.path.isfile(script_path), f"Shell script {script_path} does not exist."

def test_clean_config_contents():
    clean_config_path = "/home/user/clean_config.txt"
    assert os.path.isfile(clean_config_path), f"File {clean_config_path} does not exist."

    with open(clean_config_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "INCLUDE /home/user/project/data",
        "INCLUDE /home/user/project/src",
        "EXCLUDE .tmp",
        "EXCLUDE .o"
    ]

    assert lines == expected_lines, f"Content of {clean_config_path} is incorrect. Expected {expected_lines}, got {lines}."

def test_c_program_exists():
    source_path = "/home/user/build_manifest.c"
    bin_path = "/home/user/build_manifest"

    assert os.path.isfile(source_path), f"C source file {source_path} does not exist."
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

def test_manifest_contents_and_sorting():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    # Compute the expected hashes based on the current file contents
    expected_files = [
        "/home/user/project/data/f1.dat",
        "/home/user/project/data/f2.dat",
        "/home/user/project/src/main.c"
    ]

    expected_lines = []
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected test file {filepath} is missing."
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        expected_lines.append(f"{file_hash} {filepath}")

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected exactly {len(expected_lines)} lines in manifest (symlinks and excluded extensions "
        f"must be ignored), but got {len(actual_lines)}."
    )

    for line in expected_lines:
        assert line in actual_lines, f"Expected entry '{line}' not found in manifest."

    # The prompt specified "sorted alphabetically by the absolute file path" OR shelling out to `sort`.
    # Standard `sort` sorts by the entire line (which starts with the hash).
    # We will accept either sorting method.
    sorted_by_full_line = sorted(actual_lines)

    def extract_path(line):
        parts = line.split(maxsplit=1)
        return parts[1] if len(parts) == 2 else line

    sorted_by_path = sorted(actual_lines, key=extract_path)

    is_sorted_by_line = (actual_lines == sorted_by_full_line)
    is_sorted_by_path = (actual_lines == sorted_by_path)

    assert is_sorted_by_line or is_sorted_by_path, (
        "Manifest is not sorted. It must be sorted either by the absolute file path or "
        "by the entire line (if using the standard `sort` command)."
    )