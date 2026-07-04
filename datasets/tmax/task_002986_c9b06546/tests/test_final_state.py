# test_final_state.py

import os
import hashlib
import pytest

def test_process_script_exists_and_executable():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_unique_hashes_file_exists():
    output_path = "/home/user/unique_hashes.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_unique_hashes_content():
    output_path = "/home/user/unique_hashes.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    # Compute expected hashes based on the setup data
    payloads = [
        "server_name=app1\ntimeout=30\n",
        "server_name=app3\ntimeout=120\nmax_conn=500\n",
        "server_name=app_legacy\ndb_host=10.0.0.5\n"
    ]

    expected_hashes = sorted([hashlib.md5(p.encode('utf-8')).hexdigest() for p in payloads])

    with open(output_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_hashes, (
        f"The contents of {output_path} do not match the expected unique hashes.\n"
        f"Expected: {expected_hashes}\n"
        f"Actual: {actual_lines}"
    )