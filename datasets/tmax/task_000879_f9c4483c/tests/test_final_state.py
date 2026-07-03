# test_final_state.py

import os
import subprocess
import pytest

def test_library_path_txt():
    path_file = "/home/user/library_path.txt"
    assert os.path.exists(path_file), f"{path_file} does not exist"
    with open(path_file, "r") as f:
        content = f.read().strip()
    assert content == "/opt/legacy_ffi/libs/", f"Expected '/opt/legacy_ffi/libs/', got '{content}'"

def test_log_sanitizer_clean_corpus():
    script = "/home/user/log_sanitizer.sh"
    assert os.path.exists(script), f"{script} does not exist"

    clean_dir = "/verifier/corpus/clean"
    assert os.path.exists(clean_dir), f"{clean_dir} does not exist"

    failed_files = []
    for filename in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, filename)
        if os.path.isfile(filepath):
            result = subprocess.run(["bash", script, filepath], capture_output=True, text=True)
            if result.returncode != 0 or result.stdout.strip() != "CLEAN":
                failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} clean logs were incorrectly rejected or failed: {failed_files}"

def test_log_sanitizer_evil_corpus():
    script = "/home/user/log_sanitizer.sh"
    assert os.path.exists(script), f"{script} does not exist"

    evil_dir = "/verifier/corpus/evil"
    assert os.path.exists(evil_dir), f"{evil_dir} does not exist"

    failed_files = []
    for filename in os.listdir(evil_dir):
        filepath = os.path.join(evil_dir, filename)
        if os.path.isfile(filepath):
            result = subprocess.run(["bash", script, filepath], capture_output=True, text=True)
            if result.returncode != 1 or result.stdout.strip() != "REJECT":
                failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} evil logs bypassed the sanitizer: {failed_files}"

def test_build_success():
    project_dir = "/app/project"
    build_dir = os.path.join(project_dir, "build")
    os.makedirs(build_dir, exist_ok=True)

    cmake_res = subprocess.run(["cmake", ".."], cwd=build_dir, capture_output=True, text=True)
    assert cmake_res.returncode == 0, f"CMake configuration failed:\n{cmake_res.stderr}"

    make_res = subprocess.run(["make"], cwd=build_dir, capture_output=True, text=True)
    assert make_res.returncode == 0, f"Make build failed:\n{make_res.stderr}\n{make_res.stdout}"