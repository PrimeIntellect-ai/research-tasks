# test_final_state.py

import os
import gzip
import pytest

def test_loop_report_txt():
    report_path = "/home/user/loop_report.txt"
    assert os.path.isfile(report_path), f"Expected loop report file not found at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_loop1 = "/home/user/datasets/broken/chain/sym_loop1"
    expected_loop2_a = "/home/user/datasets/loopX/to_Y/to_X"
    expected_loop2_b = "/home/user/datasets/loopY/to_X/to_Y"

    assert expected_loop1 in lines, f"Missing {expected_loop1} in loop_report.txt"

    loop2_found = (expected_loop2_a in lines) or (expected_loop2_b in lines)
    assert loop2_found, f"Missing cross-directory loop in loop_report.txt. Expected either {expected_loop2_a} or {expected_loop2_b}"

def test_compressed_files():
    compressed_dir = "/home/user/compressed"
    assert os.path.isdir(compressed_dir), f"Compressed directory not found at {compressed_dir}"

    original_files = [
        "/home/user/datasets/expA/data1.dat",
        "/home/user/datasets/expA/sub_exp/data2.dat",
        "/home/user/datasets/expB/data3.dat",
    ]

    expected_compressed_files = []

    for orig_path in original_files:
        assert os.path.isfile(orig_path), f"Original file {orig_path} missing, setup was altered."

        stat_res = os.stat(orig_path)
        inode = stat_res.st_ino
        filename = os.path.basename(orig_path)

        comp_filename = f"{filename}_{inode}.gz"
        comp_path = os.path.join(compressed_dir, comp_filename)
        expected_compressed_files.append(comp_filename)

        assert os.path.isfile(comp_path), f"Expected compressed file {comp_path} not found."

        # Verify content
        with open(orig_path, "rb") as f:
            expected_content = f.read()

        try:
            with gzip.open(comp_path, "rb") as f:
                comp_content = f.read()
        except Exception as e:
            pytest.fail(f"Failed to decompress {comp_path}: {e}")

        assert comp_content == expected_content, f"Content mismatch in compressed file {comp_path}"

    # Verify no unexpected files are in the compressed directory
    actual_files = os.listdir(compressed_dir)
    for f in actual_files:
        assert f in expected_compressed_files, f"Unexpected file found in compressed directory: {f}"