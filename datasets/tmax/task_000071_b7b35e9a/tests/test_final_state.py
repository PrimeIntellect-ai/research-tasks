# test_final_state.py

import os
import struct
import pytest

ARTIFACTS_DIR = '/home/user/artifacts'
CORRUPT_LOG = '/home/user/corrupt.log'

def test_ignored_tmp_files():
    # Check that .tmp files are strictly ignored
    bad_txt_1 = os.path.join(ARTIFACTS_DIR, 'project_beta', 'metrics.txt.tmp')
    bad_txt_2 = os.path.join(ARTIFACTS_DIR, 'project_beta', 'metrics.bin.tmp.txt')

    assert not os.path.exists(bad_txt_1), f"Expected {bad_txt_1} not to exist, but it does."
    assert not os.path.exists(bad_txt_2), f"Expected {bad_txt_2} not to exist, but it does."

def test_corrupt_log_contents():
    assert os.path.isfile(CORRUPT_LOG), f"{CORRUPT_LOG} does not exist."

    with open(CORRUPT_LOG, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_corrupt = [
        os.path.join(ARTIFACTS_DIR, 'project_gamma', 'bad_magic.bin'),
        os.path.join(ARTIFACTS_DIR, 'project_gamma', 'truncated.bin')
    ]

    assert sorted(lines) == sorted(expected_corrupt), (
        f"Contents of {CORRUPT_LOG} do not match expected corrupted files.\n"
        f"Expected: {sorted(expected_corrupt)}\n"
        f"Found: {sorted(lines)}"
    )

def test_data1_txt_contents():
    txt_path = os.path.join(ARTIFACTS_DIR, 'project_alpha', 'v1', 'data1.txt')
    assert os.path.isfile(txt_path), f"{txt_path} was not generated."

    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["1.2346", "-9.8765", "0.0000"]
    assert lines == expected_lines, (
        f"Contents of {txt_path} do not match expected format.\n"
        f"Expected: {expected_lines}\n"
        f"Found: {lines}"
    )

def test_metrics_txt_contents():
    txt_path = os.path.join(ARTIFACTS_DIR, 'project_beta', 'metrics.txt')
    assert os.path.isfile(txt_path), f"{txt_path} was not generated."

    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["3.1416"]
    assert lines == expected_lines, (
        f"Contents of {txt_path} do not match expected format.\n"
        f"Expected: {expected_lines}\n"
        f"Found: {lines}"
    )