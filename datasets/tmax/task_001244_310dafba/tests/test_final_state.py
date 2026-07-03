# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_log_filter_executable_exists():
    executable = "/home/user/log_filter"
    assert os.path.exists(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_clean_corpus_accepted():
    executable = "/home/user/log_filter"
    clean_dir = "/home/user/logs/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.jsonl"))

    assert len(clean_files) > 0, "No clean log files found."

    failed_files = []

    for file_path in clean_files:
        with open(file_path, "rb") as f:
            input_data = f.read()

        result = subprocess.run([executable], input=input_data, capture_output=True)

        # We expect the output to match the input exactly, line by line.
        # Normalize line endings and trailing whitespace to be robust.
        input_lines = [line.strip() for line in input_data.decode('utf-8', errors='replace').strip().split('\n') if line.strip()]
        output_lines = [line.strip() for line in result.stdout.decode('utf-8', errors='replace').strip().split('\n') if line.strip()]

        if input_lines != output_lines:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified or rejected: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    executable = "/home/user/log_filter"
    evil_dir = "/home/user/logs/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.jsonl"))

    assert len(evil_files) > 0, "No evil log files found."

    failed_files = []

    for file_path in evil_files:
        with open(file_path, "rb") as f:
            input_data = f.read()

        result = subprocess.run([executable], input=input_data, capture_output=True)

        output_lines = [line.strip() for line in result.stdout.decode('utf-8', errors='replace').strip().split('\n') if line.strip()]

        if len(output_lines) > 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {', '.join(failed_files)}")

def test_vendored_library_bug_fixed():
    parser_cpp_path = "/app/vendored/jsonparse-1.2/src/parser.cpp"
    assert os.path.exists(parser_cpp_path), f"{parser_cpp_path} does not exist."

    with open(parser_cpp_path, "r") as f:
        content = f.read()

    content_no_spaces = content.replace(" ", "")
    # The deliberate bug was j<3. It should be fixed to j<4.
    assert "j<3" not in content_no_spaces, "The deliberate bug (j<3) is still present in parser.cpp"
    # Ensure it's fixed to 4 or something equivalent
    assert "j<4" in content_no_spaces or "j<=3" in content_no_spaces or "j!=4" in content_no_spaces, "The loop in parser.cpp was not fixed correctly to process 4 hex digits."