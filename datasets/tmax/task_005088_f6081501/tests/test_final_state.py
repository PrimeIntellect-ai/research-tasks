# test_final_state.py

import os
import pytest

def test_recovered_key_file():
    key_path = "/home/user/recovered_key.txt"
    assert os.path.exists(key_path), f"Recovered key file missing at {key_path}"
    with open(key_path, 'r') as f:
        content = f.read().strip()
    assert content == "8842109", f"Recovered key is incorrect. Expected '8842109', got '{content}'"

def test_decrypt_c_and_binary():
    c_path = "/home/user/decrypt.c"
    bin_path = "/home/user/decrypt"
    assert os.path.exists(c_path), f"Decryption C source code missing at {c_path}"
    assert os.path.exists(bin_path), f"Compiled decryption binary missing at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Decryption binary at {bin_path} is not executable"

def test_recovered_files_metric():
    recovered_dir = '/home/user/recovered_files'
    truth_dir = '/app/hidden_original'

    assert os.path.isdir(recovered_dir), f"Recovered files directory missing at {recovered_dir}"

    expected_files = os.listdir(truth_dir)
    assert len(expected_files) > 0, "No original files found in truth directory to compare against."

    matched_files = 0
    for f in expected_files:
        truth_path = os.path.join(truth_dir, f)
        recovered_path = os.path.join(recovered_dir, f)

        if not os.path.exists(recovered_path):
            continue

        with open(truth_path, 'rb') as t_file, open(recovered_path, 'rb') as r_file:
            if t_file.read() == r_file.read():
                matched_files += 1

    accuracy = matched_files / len(expected_files)
    assert accuracy >= 1.0, f"Metric: {accuracy}. Expected accuracy >= 1.0. Some files were not correctly decrypted or are missing."