# test_final_state.py

import os
import stat
import pytest

BASE_DIR = "/home/user/telemetry_pipeline"

def test_decoder_binary_exists_and_executable():
    bin_path = os.path.join(BASE_DIR, "bin", "decoder")
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."

    st = os.stat(bin_path)
    assert st.st_mode & stat.S_IXUSR, f"Binary {bin_path} is not executable."

def test_decoded_output_exists():
    decoded_path = os.path.join(BASE_DIR, "decoded_output.txt")
    assert os.path.isfile(decoded_path), f"File {decoded_path} is missing. Did you run the orchestrator and save its output?"

def test_sorted_output_matches_expected():
    expected_path = os.path.join(BASE_DIR, "expected.txt")
    sorted_path = os.path.join(BASE_DIR, "sorted_output.txt")

    assert os.path.isfile(expected_path), f"Expected file {expected_path} is missing."
    assert os.path.isfile(sorted_path), f"Sorted output file {sorted_path} is missing."

    with open(expected_path, "r") as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    with open(sorted_path, "r") as f:
        sorted_lines = [line.strip() for line in f if line.strip()]

    assert sorted_lines == expected_lines, "The contents of sorted_output.txt do not match expected.txt."

def test_diff_patch_valid():
    patch_path = os.path.join(BASE_DIR, "diff.patch")
    assert os.path.isfile(patch_path), f"Patch file {patch_path} is missing."

    with open(patch_path, "r") as f:
        patch_content = f.read()

    # A valid unified diff for identical files is either empty or contains only file headers.
    # It should not contain additions or deletions of data lines.
    data_additions = [line for line in patch_content.splitlines() if line.startswith('+') and not line.startswith('+++')]
    data_deletions = [line for line in patch_content.splitlines() if line.startswith('-') and not line.startswith('---')]

    assert not data_additions and not data_deletions, "diff.patch shows differences between expected.txt and sorted_output.txt."