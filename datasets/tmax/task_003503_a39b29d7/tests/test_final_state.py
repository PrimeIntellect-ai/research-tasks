# test_final_state.py

import os
import subprocess
import pytest

def test_libsemver_so_built():
    so_path = "/app/libsemver-v1.0.0/libsemver.so"
    assert os.path.isfile(so_path), f"Expected shared library {so_path} was not built."

def test_version_filter_executable_exists():
    filter_path = "/home/user/version_filter"
    assert os.path.isfile(filter_path), f"Executable {filter_path} does not exist."
    assert os.access(filter_path, os.X_OK), f"File {filter_path} is not executable."

def test_version_filter_clean_corpus():
    filter_path = "/home/user/version_filter"
    clean_in = "/app/corpus/clean/good_versions.txt"
    clean_out = "/tmp/clean_out.txt"

    if os.path.exists(clean_out):
        os.remove(clean_out)

    result = subprocess.run([filter_path, clean_in, clean_out], capture_output=True, text=True)
    assert result.returncode == 0, f"version_filter failed on clean corpus with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(clean_out), f"Output file {clean_out} was not created."

    with open(clean_in, 'r') as f:
        expected_lines = f.read().splitlines()

    with open(clean_out, 'r') as f:
        actual_lines = f.read().splitlines()

    assert actual_lines == expected_lines, "Clean corpus was modified or not fully preserved."

def test_version_filter_evil_corpus():
    filter_path = "/home/user/version_filter"
    evil_in = "/app/corpus/evil/bad_versions.txt"
    evil_out = "/tmp/evil_out.txt"

    if os.path.exists(evil_out):
        os.remove(evil_out)

    result = subprocess.run([filter_path, evil_in, evil_out], capture_output=True, text=True)
    assert result.returncode == 0, f"version_filter failed (crashed?) on evil corpus with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(evil_out), f"Output file {evil_out} was not created."

    with open(evil_out, 'r') as f:
        actual_lines = f.read().splitlines()

    # Strip out any empty lines if the script just writes newlines, but strictly it should be completely empty or just empty lines
    actual_lines = [line for line in actual_lines if line.strip()]
    assert len(actual_lines) == 0, f"Evil corpus bypassed the filter. {len(actual_lines)} evil lines were accepted."