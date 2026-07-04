# test_final_state.py
import os
import subprocess
import pytest

def run_filter(artifact_path):
    script_path = "/home/user/filter.py"
    result = subprocess.run(["python3", script_path, artifact_path], capture_output=True)
    return result.returncode

def test_filter_exists():
    assert os.path.isfile("/home/user/filter.py"), "The script /home/user/filter.py does not exist."

def test_clean_corpus():
    clean_dirs = ["/home/user/corpus/clean", "/tmp/test_corpus/clean"]
    failed_files = []
    total_files = 0

    for clean_dir in clean_dirs:
        if not os.path.isdir(clean_dir):
            continue
        for filename in os.listdir(clean_dir):
            filepath = os.path.join(clean_dir, filename)
            if os.path.isfile(filepath):
                total_files += 1
                exit_code = run_filter(filepath)
                if exit_code != 0:
                    failed_files.append(filename)

    assert len(failed_files) == 0, f"{len(failed_files)} of {total_files} clean modified/rejected. Offending files: {', '.join(failed_files)}"

def test_evil_corpus():
    evil_dirs = ["/home/user/corpus/evil", "/tmp/test_corpus/evil"]
    failed_files = []
    total_files = 0

    for evil_dir in evil_dirs:
        if not os.path.isdir(evil_dir):
            continue
        for filename in os.listdir(evil_dir):
            filepath = os.path.join(evil_dir, filename)
            if os.path.isfile(filepath):
                total_files += 1
                exit_code = run_filter(filepath)
                if exit_code != 1:
                    failed_files.append(filename)

    assert len(failed_files) == 0, f"{len(failed_files)} of {total_files} evil bypassed. Offending files: {', '.join(failed_files)}"