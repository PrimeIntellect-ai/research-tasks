# test_final_state.py

import os
import zlib
import base64
import pytest

def test_custom_compress_script_exists():
    script_path = "/home/user/custom_compress.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_archive_vault_contents():
    vault_path = "/home/user/archive_vault.txt"
    assert os.path.isfile(vault_path), f"The output file {vault_path} does not exist."

    # Dynamically compute the expected contents
    repo_dir = "/home/user/binary_repo"
    dat_files = []
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".dat"):
                dat_files.append(os.path.join(root, file))

    dat_files.sort()

    expected_lines = []
    for filepath in dat_files:
        expected_lines.append(filepath.encode('utf-8'))
        with open(filepath, 'rb') as f:
            data = f.read()
        compressed = zlib.compress(data, level=9)
        encoded = base64.b64encode(compressed)
        expected_lines.append(encoded)

    expected_content = b"\n".join(expected_lines) + b"\n" if expected_lines else b""

    with open(vault_path, 'rb') as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The contents of archive_vault.txt do not match the expected output."