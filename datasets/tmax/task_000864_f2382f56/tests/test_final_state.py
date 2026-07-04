# test_final_state.py

import os
import pytest

def test_recovered_txt_exists_and_correct():
    """Verify that recovered.txt exists and contains the exact flag."""
    recovered_path = "/home/user/recovered.txt"
    assert os.path.isfile(recovered_path), f"File not found: {recovered_path}"

    with open(recovered_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{0p3n_r3d1r3ct_t0_c0mpr0m1s3}"
    assert content == expected_flag, f"Content of {recovered_path} is incorrect. Expected '{expected_flag}', got '{content}'"

def test_decrypt_go_exists():
    """Verify that the student created the decrypt.go script."""
    script_path = "/home/user/decrypt.go"
    assert os.path.isfile(script_path), f"Go script not found: {script_path}"