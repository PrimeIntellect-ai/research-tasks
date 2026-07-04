# test_final_state.py
import os
import subprocess
import pytest

def test_filter_binary_exists():
    """Ensure the Go program has been compiled and is executable."""
    binary_path = "/home/user/filter"
    assert os.path.isfile(binary_path), f"Compiled Go binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Compiled Go binary {binary_path} is not executable."

def test_clean_corpus():
    """Ensure all clean FASTA files are accepted (exit code 0)."""
    clean_dir = "/app/clean"
    binary_path = "/home/user/filter"
    assert os.path.isdir(clean_dir), f"Clean directory {clean_dir} is missing."

    failed_files = []
    total_files = 0

    for filename in sorted(os.listdir(clean_dir)):
        filepath = os.path.join(clean_dir, filename)
        if os.path.isfile(filepath):
            total_files += 1
            result = subprocess.run([binary_path, filepath], capture_output=True)
            if result.returncode != 0:
                failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {total_files} clean files rejected (modified/failed). Offending files: {', '.join(failed_files)}"

def test_evil_corpus():
    """Ensure all evil FASTA files are rejected (exit code 1)."""
    evil_dir = "/app/evil"
    binary_path = "/home/user/filter"
    assert os.path.isdir(evil_dir), f"Evil directory {evil_dir} is missing."

    failed_files = []
    total_files = 0

    for filename in sorted(os.listdir(evil_dir)):
        filepath = os.path.join(evil_dir, filename)
        if os.path.isfile(filepath):
            total_files += 1
            result = subprocess.run([binary_path, filepath], capture_output=True)
            if result.returncode != 1:
                failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {total_files} evil files bypassed (accepted). Offending files: {', '.join(failed_files)}"