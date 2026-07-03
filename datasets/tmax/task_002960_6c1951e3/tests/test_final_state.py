# test_final_state.py

import os
import glob
import pytest

def test_tmp_processing_empty():
    tmp_dir = "/home/user/tmp_processing"
    assert os.path.isdir(tmp_dir), f"Directory {tmp_dir} is missing."
    files = os.listdir(tmp_dir)
    assert len(files) == 0, f"Temporary directory {tmp_dir} is not empty. Contains: {files}"

def test_clean_data_files():
    clean_dir = "/home/user/dataset_clean"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} is missing."

    files = sorted(os.listdir(clean_dir))
    expected_files = [f"clean_data_a{chr(ord('a') + i)}" for i in range(8)]

    assert files == expected_files, f"Expected files {expected_files}, but found {files}"

def test_clean_data_contents():
    clean_dir = "/home/user/dataset_clean"
    files = sorted(glob.glob(os.path.join(clean_dir, "clean_data_*")))

    all_lines = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                lines = fp.readlines()
                # Check that each file has 100 lines except the last one
                if f == files[-1]:
                    assert len(lines) == 50, f"Expected 50 lines in {f}, got {len(lines)}"
                else:
                    assert len(lines) == 100, f"Expected 100 lines in {f}, got {len(lines)}"
                all_lines.extend(lines)
        except UnicodeDecodeError:
            pytest.fail(f"File {f} is not properly encoded in UTF-8.")

    assert len(all_lines) == 750, f"Expected exactly 750 lines across all files, got {len(all_lines)}"

    # Verify exact contents to ensure correct sorting and decoding
    expected_lines = []
    for i in range(1, 251):
        expected_lines.append(f"Data ISO A line {i}: naïve résumé\n")
    for i in range(1, 251):
        expected_lines.append(f"Data U16 B line {i}: こんにちは\n")
    for i in range(1, 251):
        expected_lines.append(f"Data ISO C line {i}: façade\n")

    for i, (actual, expected) in enumerate(zip(all_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1}: expected {repr(expected)}, got {repr(actual)}"