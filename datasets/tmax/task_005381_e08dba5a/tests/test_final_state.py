# test_final_state.py

import os
import subprocess
import pytest

def test_failure_count():
    count_file = "/home/user/failure_count.txt"
    assert os.path.isfile(count_file), f"File {count_file} does not exist."
    with open(count_file, "r") as f:
        content = f.read().strip()
    assert content == "14", f"Expected failure count to be '14', but got '{content}'."

def test_query_filter_executable():
    executable = "/home/user/query_filter"
    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_query_filter_clean_corpus():
    executable = "/home/user/query_filter"
    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist."

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, f"No files found in {clean_dir}."

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "rb") as f:
            query = f.read()

        result = subprocess.run([executable], input=query, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()

        if output != "ACCEPT":
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean queries rejected. Offending files: {', '.join(failed_files)}")

def test_query_filter_evil_corpus():
    executable = "/home/user/query_filter"
    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), f"Directory {evil_dir} does not exist."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, f"No files found in {evil_dir}."

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "rb") as f:
            query = f.read()

        result = subprocess.run([executable], input=query, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()

        if output != "REJECT":
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil queries bypassed (accepted). Offending files: {', '.join(failed_files)}")