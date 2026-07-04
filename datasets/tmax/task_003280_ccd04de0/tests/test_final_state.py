# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_txt_exists_and_length():
    """Verify that /home/user/recovered.txt exists and contains exactly 1000 lines."""
    file_path = "/home/user/recovered.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1000, f"Expected 1000 lines in {file_path}, but found {len(lines)}."

def test_mre_txt_content():
    """Verify that /home/user/mre.txt contains the exact crash-inducing line."""
    file_path = "/home/user/mre.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_line = "[642] INFO ACTION=UPDATE PAYLOAD=tiny"
    assert content == expected_line, f"Content of {file_path} is incorrect. Expected '{expected_line}', got '{content}'."

def test_process_logs_fixed_executable():
    """Verify that /home/user/process_logs_fixed exists and is executable."""
    file_path = "/home/user/process_logs_fixed"
    assert os.path.isfile(file_path), f"Executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_process_logs_fixed_runs_successfully():
    """Verify that running process_logs_fixed with mre.txt exits cleanly."""
    executable_path = "/home/user/process_logs_fixed"
    input_file = "/home/user/mre.txt"

    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.path.isfile(input_file), f"Input file {input_file} is missing."

    with open(input_file, "r") as f:
        result = subprocess.run(
            [executable_path],
            stdin=f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    assert result.returncode == 0, f"Running {executable_path} failed with exit code {result.returncode}. Stderr: {result.stderr.decode('utf-8', errors='replace')}"